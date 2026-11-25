---
name: vintage-chinese-illustration
version: 1.0.0
display_name: 老电影风格插画（无字版）
display_name_en: Vintage Chinese Illustration (Text-Free)
description: 生成无文字、无海报版式、无书页折痕与边框的中国老电影手绘插画时使用。当用户要求“老电影风格插画”“复古手绘人物/场景”“旧宣传画质感但不要字/不要海报排版/不要旧书页效果”，或需要干净画幅的年代感插画时触发。提供纯插画参考图、提示词配方、图生图流程与细腻质感脚本。
description_zh: 用 1950–1980 年代中国老电影海报与宣传画的手绘水粉质感作画，但画面里没有片名、没有说明文字、没有画框分格，也没有旧书折痕与页边框，输出一张画幅铺满的年代感插画。适合文章配图、封面底图、角色设定图。
description_en: Paints 1950s–1980s Chinese film-poster and propaganda-art gouache illustrations with no text, no captions, no frames or panels, and no book creases or page borders. Outputs a clean full-bleed vintage illustration for article images, cover art, or character design.
agent_created: true
---

# 老电影风格插画（无字版）

## 概览

复刻老电影海报与老宣传画的绘画质感，但去掉海报作为印刷品的所有外部装置：没有片名、没有小字说明、没有画框、没有分格剧照、没有商标与水印；同时去掉旧书扫描件的物理痕迹：没有纸张折痕、撕裂纸边、卷页、页边框与暗角。产出是一张画幅铺满、可以独立使用的年代感插画。

## 何时使用

- 用户要“同风格，但不要海报文字/画框/排版”的插画。
- 用户要老电影质感的人物肖像、生活场景、劳动场景、家庭场景配图。
- 用户要把之前的海报方案改成纯画面，用于文章配图、封面底图或角色设定图。

## 与海报技能的区别

| 维度 | `vintage-chinese-film-poster` | 本技能 |
| --- | --- | --- |
| 文字 | 大号中文片名 + 小字说明 | 完全无文字 |
| 版式 | 主图 + 小剧照画框 + 标题区 | 单一完整画面，无画框、无分格 |
| 参考图 | 完整海报翻拍图 | 从海报中裁出的纯绘画区域 |
| 后处理 | 需要叠加中文标题 | 不包含标题叠加脚本 |

## 风格要点

- 画种：手绘水粉、宣传画、擦笔年画，粗黑或深褐勾线，平涂色块带刷痕，面部与衣褶少量晕染。
- 配色：褪色朱红、赭黄、灰蓝、墨绿、米黄纸底；低饱和、轻微偏色与套色错位。
- 材质：均匀纸底、细腻纸张颗粒、油墨网点、轻微套色错位；**不要折痕、撕裂纸边、卷页、页边框、扫描暗角**。
- 构图：主体居于画面中心或三分线，背景服务于主体；画面完整、不留标题空区。
- **硬性禁止**：任何文字或类文字笔画、标题区、说明文字块、画框、分格、小剧照拼贴、logo、水印、现代 UI 元素，以及书页折痕、撕裂纸边、卷页、旧书页边框、扫描暗角。

## 工作流程

### 1. 明确参数

提取主题、人物/场景、年代服装道具、画幅（默认竖版 2:3，场景可横版）。缺失时按“竖版 2:3 + 1970–80 年代手绘插画”假定并在交付时说明。

### 2. 选参考图

从 `assets/` 选 1–3 张，使用绝对路径。图生图最多支持 3 张输入图。

- 人物肖像：`01_gouache_portrait_woman.jpg`、`02_gouache_opera_portrait.jpg`、`03_magazine_portrait_woman.jpg`、`11_opera_heroine_illustration.jpg`
- 劳动/群像：`05_workers_conversation_gouache.jpg`、`06_tibetan_family_gouache.jpg`、`07_festival_children_gouache.jpg`、`10_courtyard_scene_gouache.jpg`
- 月份牌式女性：`08_calendar_boat_lady.jpg`、`09_calendar_flowers_lady.jpg`
- 场景/叙事：`04_desert_rider_gouache.jpg`、`10_courtyard_scene_gouache.jpg`

### 3. 构造提示词

读取 `references/prompt-recipes.md`，按“主体 + 年代服装道具 + 手绘画种 + 构图 + 褪色配色 + 细腻颗粒 + 无文字无画框无书页痕迹约束 + 负向词”顺序写。务必显式加入“画面中不出现任何文字、字母、数字、标题、画框、分格、拼贴小图、水印；画面铺满画幅，没有纸张折痕、撕裂纸边、卷页、旧书页边框或扫描暗角”。

### 4. 调用图像生成

图像生成会额外消耗积分，单张约 5–10 积分，**调用前必须先告知用户这一消耗**。随后：

1. 若当前会话未加载 `ImageGen` 的调用格式，先 `ToolSearch(tool_names=["ImageGen"])` 加载。
2. 通过 `DeferExecuteTool` 调用 `ImageGen`，传 `prompt`、`size`、`quality: "high"`。
3. 图生图时传 `image1`/`image2`/`image3` 为选好的绝对路径，`input_fidelity: "high"` 保持绘画质感；需要更多变化时用 `"medium"`。
4. 设置 `output_dir` 到当前工作区。
5. 自查是否有文字、画框、分格或拼贴残留；若有，加强负向词或换参考图重出，不要用涂改方式处理。

### 5. 细腻质感（可选）

生成图通常已带颜料质感。需要更统一的颗粒感时运行脚本；脚本只叠加细腻颗粒与轻微褪色，**不会添加折痕、页边框或暗角**：

```bash
python3 <技能目录>/scripts/age_poster.py 输入图.png 输出图.png --strength 0.3
```

### 6. 交付

用 `present_files` 打开成品，并说明画幅、参考图、是否做了颗粒处理，以及“无文字、无书页痕迹”约束的执行情况。

## 边界

- 只复刻视觉语言，不生成现实政治人物、敏感政治事件或易误导为真实历史宣传品的内容。
- 不复刻真实商标、明星肖像用于商业用途。

## 资源

- `assets/`：11 张从老海报中裁出的纯绘画参考图，已去除文字与画框。
- `references/style-guide.md`：插画版风格拆解与参考图说明。
- `references/prompt-recipes.md`：无字插画提示词模板与负向词。
- `scripts/age_poster.py`：可选细腻颗粒脚本，不添加折痕、页边框或暗角。
