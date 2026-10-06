# 视频提示词（fixture · slot_order_check 专用：E1 参考槽顺序）

> SHOT-010：起始帧未产出，占位起始帧槽排在第 1 位（E1 原始错误），正文还引用了 <Picture 1>。
> SHOT-011：同样未产出，但占位放在末位（E1 修正写法）→ 删除后天然连续。
> SHOT-012：PLACEHOLDER 槽夹在中间。
> SHOT-013：元数据 `占位: 1` 显式标记第 1 槽为占位。
> SHOT-014：first_frame 指向了别的镜（复制粘贴残留）。

## SHOT-010
- 时长: 8.00
- 帧数: 192
- first_frame: —
- references: 1=REF-SHOT010-START; 2=CHR-SUXIAO-BOARD; 3=CHR-STONEGOD-BOARD

```h3
subject_definitions:
  [S1] the swordswoman on the RIGHT <Picture 2>
  [S2] the stone god on the LEFT <Picture 3>
summary:
  Same clearing as <Picture 1>.
```

## SHOT-011
- 时长: 8.00
- 帧数: 192
- first_frame: —
- references: 1=CHR-SUXIAO-BOARD; 2=CHR-STONEGOD-BOARD; 3=REF-SHOT011-START

```h3
subject_definitions:
  [S1] the swordswoman on the RIGHT <Picture 1>
  [S2] the stone god on the LEFT <Picture 2>
```

## SHOT-012
- 时长: 8.00
- 帧数: 192
- first_frame: REF-SHOT012-START
- references: 1=CHR-SUXIAO-BOARD; 2=PLACEHOLDER-SHOT012-START; 3=REF-SHOT011-START

```h3
subject_definitions:
  [S1] the swordswoman on the RIGHT <Picture 1>
summary:
  Same clearing as <Picture 3>.
```

## SHOT-013
- 时长: 8.00
- 帧数: 192
- first_frame: REF-SHOT013-START
- 占位: 1
- references: 1=REF-SHOT013-START; 2=CHR-SUXIAO-BOARD

```h3
subject_definitions:
  [S1] the swordswoman in the center <Picture 2>
```

## SHOT-014
- 时长: 8.00
- 帧数: 192
- first_frame: REF-SHOT010-START
- references: 1=CHR-SUXIAO-BOARD

```h3
subject_definitions:
  [S1] the swordswoman in the center <Picture 1>
```
