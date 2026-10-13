# 随机信号分析（SSA）学习资料

《随机信号分析（第 5 版）》前两章的课程学习文档。每章包含教材重排版、作业题册、作业答案、考频分析、复习习题集和习题集答案，共 **12 份文档**。每份文档同时提供可直接阅读的 PDF 和可编辑的 LaTeX 源码。

## 第 1 章

| 文档 | PDF | LaTeX 源码 |
| --- | --- | --- |
| 教材重排版（中文） | [下载 PDF](output/教材/SSA_Textbook_CH1_zh.pdf) | [查看 .tex](output/教材/SSA_Textbook_CH1_zh.tex) |
| 第一次作业题册（英文） | [下载 PDF](output/作业/SSA_Homework_1_English.pdf) | [查看 .tex](output/作业/SSA_Homework_1_English.tex) |
| 第一次作业答案（英文） | [下载 PDF](output/作业/SSA_Homework_1_Solutions_English.pdf) | [查看 .tex](output/作业/SSA_Homework_1_Solutions_English.tex) |
| 历年考频分析（中文） | [下载 PDF](output/试卷/SSA_CH1_Exam_Frequency_Report.pdf) | [查看 .tex](output/试卷/SSA_CH1_Exam_Frequency_Report.tex) |
| 复习习题集（英文） | [下载 PDF](output/试卷/SSA_CH1_Review_Problem_Set.pdf) | [查看 .tex](output/试卷/SSA_CH1_Review_Problem_Set.tex) |
| 习题集答案（中文） | [下载 PDF](output/试卷/SSA_CH1_Review_Solutions_zh.pdf) | [查看 .tex](output/试卷/SSA_CH1_Review_Solutions_zh.tex) |

## 第 2 章

| 文档 | PDF | LaTeX 源码 |
| --- | --- | --- |
| 教材重排版（中文） | [下载 PDF](output/教材/SSA_Textbook_CH2_zh.pdf) | [查看 .tex](output/教材/SSA_Textbook_CH2_zh.tex) |
| 第二次作业题册（英文） | [下载 PDF](output/作业/SSA_Homework_2_English.pdf) | [查看 .tex](output/作业/SSA_Homework_2_English.tex) |
| 第二次作业答案（英文） | [下载 PDF](output/作业/SSA_Homework_2_Solutions_English.pdf) | [查看 .tex](output/作业/SSA_Homework_2_Solutions_English.tex) |
| 历年考频分析（中文） | [下载 PDF](output/试卷/SSA_CH2_Exam_Frequency_Report.pdf) | [查看 .tex](output/试卷/SSA_CH2_Exam_Frequency_Report.tex) |
| 复习习题集（英文） | [下载 PDF](output/试卷/SSA_CH2_Review_Problem_Set.pdf) | [查看 .tex](output/试卷/SSA_CH2_Review_Problem_Set.tex) |
| 习题集答案（中文） | [下载 PDF](output/试卷/SSA_CH2_Review_Solutions_zh.pdf) | [查看 .tex](output/试卷/SSA_CH2_Review_Solutions_zh.tex) |

## 文件与使用方式

- `output/教材/`：中文教材重排版。
- `output/作业/`：英文作业题册与答案。
- `output/试卷/`：考频分析、复习习题集与中文详解。
- PDF 可直接阅读；同名 `.tex` 是对应的可编辑源码。中文文档请使用 XeLaTeX 编译。为避免中间文件混入交付目录，建议把编译输出指定到单独的临时目录。

本仓库收录前两章成品、考点标注数据和文档制作技能，不包含原始教材扫描件、历年试卷PDF或构建过程中的临时文件。教材原文及相关课程材料的权利归各自权利人所有；这些文档用于课程学习与复习。

## 八套真题版更新（2026-10-13）

考频与复习材料已基于8套试卷、107个计分小问重新构建。新增四套来自 [格院往年试卷仓库](https://github.com/StrikerLeecy126/UESTC_Glasgow_College_CE_Final_Exams)；完整来源、封面日期、SHA-256及唯一主归属见 [共享试卷审计数据](output/试卷/SSA_Exam_Corpus.json)。间接涉及不重复计分。

| 章节 | 核心均值（八套） | 考频报告 | 习题集 | 中文详解 |
|---|---:|---:|---|---:|
| 第一章 | 27.50分 | 10页 | 30题 / 33页，覆盖全部11道作业 | 25页 |
| 第二章 | 15.625分 | 10页 | 27题 / 30页，覆盖全部10道作业 | 21页 |

### 页面比例与阅读方式

五份下游文档采用2048:2732竖屏比例的制作约定。作业题册和习题集用于Notability手写，保持每页一题与作答留白；作业答案、考频和中文详解按电脑阅读连续排版。此次两章报告取消逐节/逐卷强制换页，长表自动续页；两份中文详解的来源索引各一页，解答自然跨页。

已更新 [考频技能](.dsh/skills/exam-frequency-report/SKILL.md)、[作业技能](.dsh/skills/ssa-homework/SKILL.md)及配套模板和验收脚本，制作工作流见 [WORKFLOW](WORKFLOW.md)。[分页修订记录](output/工具/SSA_Pagination_Fix.md)和[八套重建记录](output/工具/SSA_Exam8_Rebuild_Progress.md)保留验收摘要；记录中提到的tmp目录为本地构建证据，不随仓库发布。
