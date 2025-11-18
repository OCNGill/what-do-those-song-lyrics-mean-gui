"""
Hardware detection module for model recommendation.
Detects CPU, RAM, GPU capabilities and recommends compatible AI models.
"""
from __future__ import annotations

import logging
import platform
from dataclasses import dataclass
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class HardwareSpecs:
    """Hardware specifications for model selection."""
    cpu_count: int
    cpu_name: str
    total_ram_gb: float
    available_ram_gb: float
    has_cuda: bool
    has_mps: bool  # Apple Metal Performance Shaders
    cuda_version: Optional[str]
    gpu_name: Optional[str]
    gpu_memory_gb: Optional[float]
    
    def __str__(self) -> str:
        specs = [
            f"CPU: {self.cpu_name} ({self.cpu_count} cores)",
            f"RAM: {self.available_ram_gb:.1f}GB available / {self.total_ram_gb:.1f}GB total",
        ]
        if self.has_cuda:
            specs.append(f"GPU: {self.gpu_name} ({self.gpu_memory_gb:.1f}GB VRAM) - CUDA {self.cuda_version}")
        elif self.has_mps:
            specs.append("GPU: Apple Silicon (Metal)")
        else:
            specs.append("GPU: None (CPU only)")
        return "\n".join(specs)


def detect_hardware() -> HardwareSpecs:
    """
    Detect system hardware capabilities.
    
    Returns:
        HardwareSpecs object with system information
    """
    import psutil
    import os
    
    # CPU detection
    cpu_count = psutil.cpu_count(logical=True)
    cpu_name = platform.processor() or "Unknown CPU"
    
    # RAM detection
    ram = psutil.virtual_memory()
    total_ram_gb = ram.total / (1024 ** 3)
    available_ram_gb = ram.available / (1024 ** 3)
    
    # GPU detection
    has_cuda = False
    has_mps = False
    cuda_version = None
    gpu_name = None
    gpu_memory_gb = None
    
    # Check for CUDA (NVIDIA)
    try:
        import torch
        if torch.cuda.is_available():
            has_cuda = True
            cuda_version = torch.version.cuda
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory_gb = torch.cuda.get_device_properties(0).total_memory / (1024 ** 3)
            logger.info("CUDA GPU detected")
    except:
        pass
    
    # Check for MPS (Apple Silicon)
    try:
        import torch
        if hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            has_mps = True
            gpu_name = "Apple Silicon"
            logger.info("Apple Silicon GPU detected")
    except:
        pass
    
    return HardwareSpecs(
        cpu_count=cpu_count,
        cpu_name=cpu_name,
        total_ram_gb=total_ram_gb,
        available_ram_gb=available_ram_gb,
        has_cuda=has_cuda,
        has_mps=has_mps,
        cuda_version=cuda_version,
        gpu_name=gpu_name,
        gpu_memory_gb=gpu_memory_gb,
    )


@dataclass
class ModelRecommendation:
    """Model recommendation with requirements."""
    model_id: str
    model_name: str
    size_mb: int
    min_ram_gb: float
    requires_gpu: bool
    recommended_for: str  # "cpu", "gpu", "high-end"
    description: str
    
    def is_compatible(self, hardware: HardwareSpecs) -> bool:
        """Check if model is compatible with hardware."""
        # Check RAM requirement
        if hardware.available_ram_gb < self.min_ram_gb:
            return False
        
        # Check GPU requirement
        if self.requires_gpu and not (hardware.has_cuda or hardware.has_mps):
            return False
        
        return True


# Pre-configured model recommendations
MODEL_CATALOG = [
    ModelRecommendation(
        model_id="google/flan-t5-small",
        model_name="FLAN-T5 Small",
        size_mb=308,
        min_ram_gb=2.0,
        requires_gpu=False,
        recommended_for="cpu",
        description="Lightweight model, perfect for CPU-only systems. Fast but basic interpretations."
    ),
    ModelRecommendation(
        model_id="google/flan-t5-base",
        model_name="FLAN-T5 Base",
        size_mb=990,
        min_ram_gb=4.0,
        requires_gpu=False,
        recommended_for="cpu",
        description="Balanced model for CPU. Better quality than Small, still reasonably fast."
    ),
    ModelRecommendation(
        model_id="google/flan-t5-large",
        model_name="FLAN-T5 Large",
        size_mb=2950,
        min_ram_gb=8.0,
        requires_gpu=False,
        recommended_for="cpu",
        description="High-quality CPU model. Requires 8GB+ RAM. Slower but excellent results."
    ),
    ModelRecommendation(
        model_id="google/flan-t5-xl",
        model_name="FLAN-T5 XL",
        size_mb=11200,
        min_ram_gb=16.0,
        requires_gpu=True,
        recommended_for="gpu",
        description="Very large model. Requires GPU with 16GB+ VRAM or 32GB+ system RAM."
    ),
    ModelRecommendation(
        model_id="facebook/bart-large-cnn",
        model_name="BART Large",
        size_mb=1630,
        min_ram_gb=6.0,
        requires_gpu=False,
        recommended_for="cpu",
        description="Good for summarization and analysis. Moderate resource usage."
    ),
]


def get_compatible_models(hardware: HardwareSpecs) -> list[ModelRecommendation]:
    """
    Get list of models compatible with current hardware.
    
    Args:
        hardware: HardwareSpecs object
        
    Returns:
        List of compatible ModelRecommendation objects, sorted by size
    """
    compatible = [model for model in MODEL_CATALOG if model.is_compatible(hardware)]
    return sorted(compatible, key=lambda m: m.size_mb)


def get_recommended_model(hardware: HardwareSpecs) -> ModelRecommendation:
    """
    Get the best recommended model for current hardware.
    
    Args:
        hardware: HardwareSpecs object
        
    Returns:
        ModelRecommendation object
    """
    compatible = get_compatible_models(hardware)
    
    if not compatible:
        # Fallback to smallest model if nothing is compatible
        return MODEL_CATALOG[0]
    
    # Logic: choose the largest compatible model that fits the hardware category
    if hardware.has_cuda or hardware.has_mps:
        # GPU available - recommend largest GPU-compatible model
        gpu_models = [m for m in compatible if m.recommended_for in ["gpu", "high-end"]]
        if gpu_models:
            return gpu_models[-1]  # Largest
    
    # CPU only - recommend medium-sized CPU model if available
    cpu_models = [m for m in compatible if m.recommended_for == "cpu"]
    if len(cpu_models) >= 2:
        return cpu_models[1]  # Second option (Base instead of Small)
    elif cpu_models:
        return cpu_models[0]
    
    return compatible[0]


if __name__ == "__main__":
    print("Detecting hardware...")
    hardware = detect_hardware()
    print("\n" + "="*60)
    print("HARDWARE SPECS")
    print("="*60)
    print(hardware)
    
    print("\n" + "="*60)
    print("RECOMMENDED MODEL")
    print("="*60)
    recommended = get_recommended_model(hardware)
    print(f"{recommended.model_name} ({recommended.model_id})")
    print(f"Size: {recommended.size_mb}MB")
    print(f"Min RAM: {recommended.min_ram_gb}GB")
    print(f"GPU Required: {'Yes' if recommended.requires_gpu else 'No'}")
    print(f"Description: {recommended.description}")
    
    print("\n" + "="*60)
    print("ALL COMPATIBLE MODELS")
    print("="*60)
    for model in get_compatible_models(hardware):
        print(f"✓ {model.model_name} - {model.size_mb}MB - {model.description}")
