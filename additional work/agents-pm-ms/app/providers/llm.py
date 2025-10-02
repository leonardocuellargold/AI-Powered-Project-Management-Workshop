"""Unified interface for large language model providers.

This module keeps the runtime simple for the workshop while allowing
attendees to plug in whichever foundation model they already have access to.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from dotenv import load_dotenv

logger = logging.getLogger(__name__)


@dataclass
class ProviderConfig:
    """Runtime configuration for the LLM provider."""

    provider: str
    model: str
    dry_run: bool = False


class LLMProvider:
    """Lightweight abstraction over OpenAI, Anthropic, and Gemini SDKs.

    The class supports a `dry_run` mode that returns synthetic outputs so the
    workshop can run end-to-end without external API calls.
    """

    _DEFAULT_MODELS: Dict[str, str] = {
        "openai": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        "anthropic": os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-latest"),
        "gemini": os.getenv("GEMINI_MODEL", "gemini-1.5-flash"),
    }

    def __init__(self, config: ProviderConfig) -> None:
        self.config = config
        self._client: Any = None

        if self.config.dry_run:
            logger.info("LLM provider running in DRY_RUN mode; no API calls will be made.")
            return

        provider = config.provider.lower()
        if provider == "openai":
            self._client = self._init_openai()
        elif provider == "anthropic":
            self._client = self._init_anthropic()
        elif provider == "gemini":
            self._client = self._init_gemini()
        else:
            raise ValueError(f"Unsupported provider '{config.provider}'.")

    @classmethod
    def from_env(cls, dry_override: Optional[bool] = None) -> "LLMProvider":
        """Create an instance from environment variables.

        The selection logic prefers the provider specified in `LLM_PROVIDER` and
        falls back to whichever API key is available.
        """

        load_dotenv()

        dry_run = dry_override if dry_override is not None else bool(int(os.getenv("DRY_RUN", "0")))

        provider_hint = os.getenv("LLM_PROVIDER")
        provider = None
        model = None

        provider_chain = [
            ("openai", os.getenv("OPENAI_API_KEY")),
            ("anthropic", os.getenv("ANTHROPIC_API_KEY")),
            ("gemini", os.getenv("GEMINI_API_KEY")),
        ]

        if provider_hint:
            provider_hint = provider_hint.lower()
            matching_key = next((key for name, key in provider_chain if name == provider_hint and key), None)
            if matching_key:
                provider = provider_hint

        if provider is None:
            provider = next((name for name, key in provider_chain if key), "openai")

        model = os.getenv(f"{provider.upper()}_MODEL", cls._DEFAULT_MODELS.get(provider, ""))

        config = ProviderConfig(provider=provider, model=model or "gpt-4o-mini", dry_run=dry_run)
        return cls(config)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def generate(
        self,
        prompt: str,
        *,
        system_prompt: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: int = 1_024,
    ) -> str:
        """Generate text from the configured provider or synthetic stub."""

        if self.config.dry_run:
            return self._mock_response(prompt, system_prompt=system_prompt)

        provider = self.config.provider.lower()
        if provider == "openai":
            return self._generate_openai(prompt, system_prompt, temperature, max_tokens)
        if provider == "anthropic":
            return self._generate_anthropic(prompt, system_prompt, temperature, max_tokens)
        if provider == "gemini":
            return self._generate_gemini(prompt, system_prompt, temperature, max_tokens)

        raise RuntimeError(f"Provider '{self.config.provider}' is not supported at runtime.")

    # ------------------------------------------------------------------
    # Provider initialisers
    # ------------------------------------------------------------------
    def _init_openai(self):
        try:
            from openai import OpenAI
        except ImportError as exc:  # pragma: no cover - defensive
            raise RuntimeError("openai SDK is not installed inside the container.") from exc

        key = os.getenv("OPENAI_API_KEY")
        if not key:
            raise RuntimeError("OPENAI_API_KEY is required for OpenAI provider.")

        return OpenAI(api_key=key)

    def _init_anthropic(self):
        try:
            import anthropic
        except ImportError as exc:  # pragma: no cover - defensive
            raise RuntimeError("anthropic SDK is not installed inside the container.") from exc

        key = os.getenv("ANTHROPIC_API_KEY")
        if not key:
            raise RuntimeError("ANTHROPIC_API_KEY is required for Anthropic provider.")

        return anthropic.Anthropic(api_key=key)

    def _init_gemini(self):
        try:
            import google.generativeai as genai
        except ImportError as exc:  # pragma: no cover - defensive
            raise RuntimeError("google-generativeai SDK is not installed inside the container.") from exc

        key = os.getenv("GEMINI_API_KEY")
        if not key:
            raise RuntimeError("GEMINI_API_KEY is required for Gemini provider.")

        genai.configure(api_key=key)
        return genai

    # ------------------------------------------------------------------
    # Per-provider generation
    # ------------------------------------------------------------------
    def _generate_openai(
        self,
        prompt: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int,
    ) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = self._client.chat.completions.create(
            model=self.config.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content.strip()

    def _generate_anthropic(
        self,
        prompt: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int,
    ) -> str:
        kwargs: Dict[str, Any] = {
            "model": self.config.model,
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
        }
        if system_prompt:
            kwargs["system"] = system_prompt

        response = self._client.messages.create(**kwargs)
        text_blocks = [block.text for block in response.content if hasattr(block, "text")]
        return "\n".join(text_blocks).strip()

    def _generate_gemini(
        self,
        prompt: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int,
    ) -> str:
        genai = self._client
        generation_config = genai.types.GenerationConfig(
            temperature=temperature,
            max_output_tokens=max_tokens,
        )
        model = genai.GenerativeModel(self.config.model, generation_config=generation_config)
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        response = model.generate_content(full_prompt)
        if not response.text:
            raise RuntimeError("Gemini response was empty.")
        return response.text.strip()

    # ------------------------------------------------------------------
    # Dry-run helper
    # ------------------------------------------------------------------
    def _mock_response(self, prompt: str, *, system_prompt: Optional[str] = None) -> str:
        """Return pseudo-deterministic text for workshop dry runs."""

        seed = (system_prompt or "") + prompt
        words = [word.strip(".,;:!?") for word in seed.split() if word.isalpha()]
        selection = words[:60] if words else ["workshop", "demo", "output"]
        unique_words = []
        for word in selection:
            lower = word.lower()
            if lower not in unique_words:
                unique_words.append(lower)

        bulleted = "\n".join(f"- {word.title()} insight" for word in unique_words[:6])
        body = (
            "This is a demonstration response generated in DRY_RUN mode. "
            "Replace it with live LLM output by providing an API key."
        )
        return f"{body}\n\n{bulleted}"
