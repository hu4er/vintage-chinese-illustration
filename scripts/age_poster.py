#!/usr/bin/env python3
"""给图像叠加细腻纸张颗粒与轻微褪色。

只做颜色与颗粒处理，不添加折痕、撕裂纸边、页边框、装裱框或扫描暗角。
"""
import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter


def subtle_grain(img, strength, seed):
    rng = np.random.default_rng(seed)
    arr = np.asarray(img.convert("RGB"), dtype=np.float32) / 255.0
    h, w = arr.shape[:2]

    # 轻微褪色与暖色调，不产生暗角
    gray = arr.mean(axis=2, keepdims=True)
    arr = gray + (arr - gray) * (1.0 - 0.16 * strength)
    tint = np.array([1.03, 1.00, 0.93], dtype=np.float32)
    arr = np.clip(arr * tint, 0, 1)

    # 细腻颗粒与极淡的低频色斑
    grain = rng.normal(0, 0.028 * strength, (h, w, 1)).astype(np.float32)
    low = rng.normal(0, 0.012 * strength, (max(1, h // 40), max(1, w // 40), 1))
    low_img = Image.fromarray(np.clip((low[:, :, 0] + 0.5) * 255, 0, 255).astype(np.uint8))
    low_img = low_img.resize((w, h), Image.Resampling.BICUBIC)
    low_arr = (np.asarray(low_img, dtype=np.float32) / 255.0 - 0.5)[:, :, None]
    arr = np.clip(arr + grain + low_arr * 0.5, 0, 1)

    out = Image.fromarray((arr * 255).astype(np.uint8), "RGB")
    return out.filter(ImageFilter.GaussianBlur(radius=0.2 * strength))


def main():
    parser = argparse.ArgumentParser(description="叠加细腻纸张颗粒与轻微褪色，不添加折痕或页边框")
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("--strength", type=float, default=0.3)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    strength = float(np.clip(args.strength, 0, 1))
    img = Image.open(args.input).convert("RGB")
    result = subtle_grain(img, strength, args.seed)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.suffix.lower() in (".jpg", ".jpeg"):
        result.save(out, "JPEG", quality=92)
    else:
        result.save(out, "PNG")
    print(f"saved: {out}")


if __name__ == "__main__":
    main()
