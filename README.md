# 随机信号分析（SSA）学习资料

《随机信号分析（第 5 版）》前三章的课程学习文档。每章包含教材重排版、作业题册、作业答案、考频分析、复习习题集和习题集答案，共 **18 份文档**。每份文档同时提供可直接阅读的 PDF 和可编辑的 LaTeX 源码。

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

本仓库收录前三章成品、考点标注数据和文档制作技能，不包含原始教材扫描件、历年试卷PDF或构建过程中的临时文件。教材原文及相关课程材料的权利归各自权利人所有；这些文档用于课程学习与复习。

## 八套真题版更新（2026-10-13）

考频与复习材料已基于8套试卷、107个计分小问重新构建。新增四套来自 [格院往年试卷仓库](https://github.com/StrikerLeecy126/UESTC_Glasgow_College_CE_Final_Exams)；完整来源、封面日期、SHA-256及唯一主归属见 [共享试卷审计数据](output/试卷/SSA_Exam_Corpus.json)。间接涉及不重复计分。

| 章节 | 核心均值（八套） | 考频报告 | 习题集 | 中文详解 |
|---|---:|---:|---|---:|
| 第一章 | 27.50分 | 10页 | 30题 / 33页，覆盖全部11道作业 | 25页 |
| 第二章 | 15.625分 | 10页 | 27题 / 30页，覆盖全部10道作业 | 21页 |

### 页面比例与阅读方式

五份下游文档采用2048:2732竖屏比例的制作约定。作业题册和习题集用于Notability手写，保持每页一题与作答留白；作业答案、考频和中文详解按电脑阅读连续排版。此次两章报告取消逐节/逐卷强制换页，长表自动续页；两份中文详解的来源索引各一页，解答自然跨页。

已更新 [考频技能](.dsh/skills/exam-frequency-report/SKILL.md)、[作业技能](.dsh/skills/ssa-homework/SKILL.md)及配套模板和验收脚本，制作工作流见 [WORKFLOW](WORKFLOW.md)。[分页修订记录](output/工具/SSA_Pagination_Fix.md)和[八套重建记录](output/工具/SSA_Exam8_Rebuild_Progress.md)保留验收摘要；记录中提到的tmp目录为本地构建证据，不随仓库发布。

## 第 3 章（2026-10-27）

第三章六件套已验收，六份 PDF 合计 **100 页**，每份配有自包含 LaTeX 源码。题册与复习题集每题一页留白，两份答案连续排版。

| 文档 | 页数 | PDF | LaTeX |
|---|---:|---|---|
| 教材重排版 | 38 | [阅读 PDF](教材/重排版/SSA_Textbook_CH3_zh.pdf) | [查看源码](教材/重排版/SSA_Textbook_CH3_zh.tex) |
| 第三次作业题册（英文） | 10 | [阅读 PDF](作业/题册与答案/SSA_Homework_3_English.pdf) | [查看源码](作业/题册与答案/SSA_Homework_3_English.tex) |
| 第三次作业详解（英文） | 6 | [阅读 PDF](作业/题册与答案/SSA_Homework_3_Solutions_English.pdf) | [查看源码](作业/题册与答案/SSA_Homework_3_Solutions_English.tex) |
| 八套考频报告（中文） | 10 | [阅读 PDF](试卷/考频与复习/SSA_CH3_Exam_Frequency_Report.pdf) | [查看源码](试卷/考频与复习/SSA_CH3_Exam_Frequency_Report.tex) |
| 复习题集（英文，21题/7天） | 23 | [阅读 PDF](试卷/考频与复习/SSA_CH3_Review_Problem_Set.pdf) | [查看源码](试卷/考频与复习/SSA_CH3_Review_Problem_Set.tex) |
| 习题集详解（中文） | 13 | [阅读 PDF](试卷/考频与复习/SSA_CH3_Review_Solutions_zh.pdf) | [查看源码](试卷/考频与复习/SSA_CH3_Review_Solutions_zh.tex) |

[下载第三章完整资料包](工具/资料包/SSA_CH3_Six_Pack_20261027.zip) · [SHA-256](工具/资料包/SSA_CH3_Six_Pack_20261027.sha256) · [交接与验收](工具/工作流记录/SSA_CH3_Handoff.md) · [逐小问考点标注与作业覆盖](试卷/考频与复习/SSA_CH3_Exam_Tagging.json)

必做：3.4、3.5、3.9、3.14、3.16、3.21、3.25；选做：3.1、3.7、3.19。复习题集完整覆盖全部10题，再补11道代表题。截止通知保留“第三章结束后一周”，未补造绝对日期。

本章八套核心分值为0/0/9/19/17/25/29/7，均值13.25分/套；最近四套均值19.50。沿用前两章唯一主归属规则，跨章不重复计分。34项精确/数值交叉检查及五份新文档的全页渲染检查已完成。3.19的非有限功率谱、重复时刻联合密度、原真题条件冲突均在解答中明示。

第三章采用本地整理后的顶层分类路径；第一、二章保留仓库既有位置及下载链接。原教材扫描件、原卷PDF、个人提交稿和临时构建文件不随本次上传。
