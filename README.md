# Shape Key Bone Control Creator

[English](#english) | [한글](#korean) | [日本語](#japanese) | [中文](#chinese)

<code style="color: #0366d6; background-color: #f6f8fa; padding: 16px; display: block;">
Shape Key Bone Control Creator is a Blender add-on that helps you visualize and control shape keys through bone-based sliders.
</code>

## Preview / 미리보기 / プレビュー / 预览

[![Video Tutorial](https://img.youtube.com/vi/ZL2vitS9E3M/maxresdefault.jpg)](https://youtu.be/ZL2vitS9E3M)

<details>
<summary><code style="color: #d73a49; font-size: 1.1em;">▶️ Watch on YouTube / 유튜브에서 보기 / YouTubeで見る / 在YouTube上观看</code></summary>

[Shape Keys Bone And Custom Shape Creater - Blender Face Animation Add-on](https://youtu.be/ZL2vitS9E3M)
</details>

## Version History / 버전 기록 / バージョン履歴 / 版本历史

<details>
<summary><code style="color: #0366d6; font-size: 1.1em;">📌 v1.1.2 (2025-02-08)</code></summary>

![Shape Key UI Preview](./images/shape_key_ui_preview.png)
![Driver Adjustment](./images/driver_adjustment.png)

<details>
<summary><code style="color: #28a745;">🇺🇸 English</code></summary>

**Shape Key UI Improvements**
- Add display functionality for all visible mesh shape keys
  - Show all shape key meshes visible in scene
  - Improve shape key list visibility
- Enhance driver UI stability
  - Add existence check for animation_data and drivers
  - Handle errors for shape keys without drivers
- Improve driver influence adjustment UI
  - Add mesh name, shape key name, and transform type to popup dialog
  - Enhance slider UI for better control

**Bug Fixes**
- Fix error occurring when processing shape keys without drivers
- Improve error handling in shape key operations
- Add proper checks for animation data existence
</details>

<details>
<summary><code style="color: #28a745;">🇰🇷 한글</code></summary>

**쉐이프 키 UI 개선**
- 모든 가시적인 메쉬의 쉐이프 키 표시 기능 추가
  - 씬에서 보이는 모든 쉐이프 키 메쉬 표시
  - 쉐이프 키 리스트 가시성 개선
- 드라이버 UI 안정성 향상
  - animation_data와 drivers 존재 여부 체크 추가
  - 드라이버가 없는 쉐이프 키에 대한 에러 처리
- 드라이버 영향도 조정 UI 개선
  - 팝업 다이얼로그에 메쉬 이름, 쉐이프 키 이름, 변환 타입 표시
  - 더 나은 제어를 위한 슬라이더 UI 개선

**버그 수정**
- 드라이버가 없는 쉐이프 키 처리 시 발생하는 에러 수정
- 쉐이프 키 작업의 에러 처리 개선
- 애니메이션 데이터 존재 여부 체크 추가
</details>

<details>
<summary><code style="color: #28a745;">🇯🇵 日本語</code></summary>

**シェイプキーUI改善**
- すべての可視メッシュのシェイプキー表示機能を追加
  - シーンに表示されているすべてのシェイプキーメッシュを表示
  - シェイプキーリストの可視性を改善
- ドライバーUIの安定性向上
  - animation_dataとdriversの存在チェックを追加
  - ドライバーのないシェイプキーのエラー処理
- ドライバーの影響度調整UI改善
  - ポップアップダイアログにメッシュ名、シェイプキー名、変換タイプを表示
  - より良い制御のためのスライダーUI改善

**バグ修正**
- ドライバーのないシェイプキー処理時のエラーを修正
- シェイプキー操作のエラー処理を改善
- アニメーションデータの存在チェックを追加
</details>

<details>
<summary><code style="color: #28a745;">🇨🇳 中文</code></summary>

**形态键UI改进**
- 添加显示所有可见网格形态键的功能
  - 显示场景中所有可见的形态键网格
  - 改进形态键列表可见性
- 增强驱动器UI稳定性
  - 添加animation_data和drivers存在性检查
  - 处理没有驱动器的形态键错误
- 改进驱动器影响度调整UI
  - 在弹出对话框中显示网格名称、形态键名称和变换类型
  - 改进滑块UI以获得更好的控制

**错误修复**
- 修复处理没有驱动器的形态键时出现的错误
- 改进形态键操作的错误处理
- 添加动画数据存在性检查
</details>
</details>

<details>
<summary><code style="color: #0366d6; font-size: 1.1em;">📌 v1.1 (2025-02-08)</code></summary>

<details>
<summary><code style="color: #28a745;">🇺🇸 English</code></summary>

- Added head bone parenting option for shape key controllers
- Auto-select Basis shape key after driver operations
- Enhanced widget and bone cleanup during deletion
- Improved driver management system
- Added support for widget parenting to head bone
</details>

<details>
<summary><code style="color: #28a745;">🇰🇷 한글</code></summary>

- 쉐이프 키 컨트롤러의 헤드 본 페런팅 옵션 추가
- 드라이버 작업 후 자동으로 Basis 쉐이프 키 선택
- 삭제 시 위젯과 본 정리 기능 강화
- 드라이버 관리 시스템 개선
- 헤드 본에 대한 위젯 페런팅 지원 추가
</details>

<details>
<summary><code style="color: #28a745;">🇯🇵 日本語</code></summary>

- シェイプキーコントローラーにヘッドボーンペアレントオプションを追加
- ドライバー操作後にベーシスシェイプキーを自動選択
- 削除時のウィジェットとボーンのクリーンアップを強化
- ドライバー管理システムを改善
- ヘッドボーンへのウィジェットペアレントをサポート
</details>

<details>
<summary><code style="color: #28a745;">🇨🇳 中文</code></summary>

- 为形态键控制器添加头部骨骼父级选项
- 驱动器操作后自动选择基础形态键
- 增强删除时的部件和骨骼清理
- 改进驱动器管理系统
- 添加部件到头部骨骼的父级支持
</details>
</details>

<details>
<summary><code style="color: #0366d6; font-size: 1.1em;">📌 v1.0 (2025-02-07)</code></summary>

<details>
<summary><code style="color: #28a745;">🇺🇸 English</code></summary>

- Initial release
- Basic shape key bone creation
- Widget system implementation
- Driver system setup
</details>
</details>

<a name="english"></a>
# Shape Key Bone Control Creator

<code style="color: #0366d6; background-color: #f6f8fa; padding: 16px; display: block;">
Shape Key Bone Control Creator is a Blender add-on that helps you visualize and control shape keys through bone-based sliders.
</code>

<details>
<summary><code style="color: #0366d6; font-size: 1.1em;">✨ Features</code></summary>

- Visualize shape keys as 3D text
- Control shape keys through slider widgets
- Metarig and Rigify rig support
- Bone-based control system
- Automatic driver setup
</details>

<details>
<summary><code style="color: #28a745; font-size: 1.1em;">📥 Installation</code></summary>

1. Start Blender
2. Go to Edit > Preferences > Add-ons
3. Click "Install..."
4. Select the downloaded ZIP file
5. Activate the add-on
</details>

<details>
<summary><code style="color: #5f2eea; font-size: 1.1em;">🎯 How to Use</code></summary>

### 1. Initial Setup
- Find View3D > Sidebar > Shape Key Tools panel

### 2. Setup Metarig and Rigify rig
- Click "Find Metarig" to auto-detect metarig
- Click "Find Rigify" to auto-detect rigify rig

### 3. Create shape key bone
- Click "Add Shape Key Bone"
- Select target mesh and shape key
- Set transform type and influence
- Choose text widget creation options

### 4. Widget management
- Click "Recreate Templates" to reset templates
- Click "Assign Widget To Bone" for manual widget assignment
</details>

<details>
<summary><code style="color: #6f42c1; font-size: 1.1em;">🔧 Feature Details</code></summary>

### Shape Key Bone Creation
- Create new bone in metarig
- Auto-setup rigify parameters
- Auto-connect drivers
- Auto-generate text widgets

### Widget System
- Composed of handle, slider, and text
- Synchronized with bone movement
- Custom text support

### Driver System
- Location, rotation, scale-based control
- User-defined influence settings
- Automatic driver setup
</details>

<details>
<summary><code style="color: #d73a49; font-size: 1.1em;">⚙️ System Requirements</code></summary>

- Blender 4.0 or higher
- Rigify add-on required
</details>

<details>
<summary><code style="color: #24292e; font-size: 1.1em;">📜 License</code></summary>

GNU General Public License v3.0 (GPL-3.0)

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
</details>

---

<a name="korean"></a>
# Shape Key Bone Control Creator

<code style="color: #0366d6; background-color: #f6f8fa; padding: 16px; display: block;">
쉐이프 키 본 컨트롤 생성기는 Blender 애드온으로, 쉐이프 키를 본 기반 슬라이더로 시각화하고 조작할 수 있게 해주는 도구입니다.
</code>

<details>
<summary><code style="color: #0366d6; font-size: 1.1em;">✨ 주요 기능</code></summary>

- 쉐이프 키를 3D 텍스트로 시각화
- 슬라이더 위젯을 통한 쉐이프 키 제어
- 메타리그와 리기파이 리그 지원
- 본 기반 컨트롤 시스템
- 드라이버 자동 설정
</details>

<details>
<summary><code style="color: #28a745; font-size: 1.1em;">📥 설치 방법</code></summary>

1. Blender를 실행합니다
2. Edit > Preferences > Add-ons로 이동합니다
3. "Install..." 버튼을 클릭합니다
4. 다운로드 받은 ZIP 파일을 선택합니다
5. 애드온을 활성화합니다
</details>

<details>
<summary><code style="color: #5f2eea; font-size: 1.1em;">🎯 사용 방법</code></summary>

### 1. 초기 설정
- View3D > Sidebar > Shape Key Tools 패널을 찾습니다

### 2. 메타리그와 리기파이 리그 설정
- "Find Metarig" 버튼으로 메타리그 자동 검색
- "Find Rigify" 버튼으로 리기파이 리그 자동 검색

### 3. 쉐이프 키 본 생성
- "Add Shape Key Bone" 버튼 클릭
- 대상 메쉬와 쉐이프 키 선택
- 변형 타입과 영향도 설정
- 텍스트 위젯 생성 옵션 선택

### 4. 위젯 관리
- "Recreate Templates" 버튼으로 템플릿 초기화
- "Assign Widget To Bone" 버튼으로 위젯 수동 할당
</details>

<details>
<summary><code style="color: #6f42c1; font-size: 1.1em;">🔧 주요 기능 설명</code></summary>

### 쉐이프 키 본 생성
- 메타리그에 새로운 본 생성
- 리기파이 파라미터 자동 설정
- 드라이버 자동 연결
- 텍스트 위젯 자동 생성

### 위젯 시스템
- 핸들, 슬라이더, 텍스트로 구성
- 본 움직임과 연동
- 커스텀 텍스트 지원

### 드라이버 시스템
- 위치, 회전, 스케일 기반 제어
- 사용자 정의 영향도 설정
- 자동 드라이버 설정
</details>

<details>
<summary><code style="color: #d73a49; font-size: 1.1em;">⚙️ 시스템 요구사항</code></summary>

- Blender 4.0 이상
- 리기파이 애드온 필요
</details>

<details>
<summary><code style="color: #24292e; font-size: 1.1em;">📜 라이선스</code></summary>

GNU General Public License v3.0 (GPL-3.0)

이 프로그램은 자유 소프트웨어입니다. GNU 일반 공중 사용 허가서(GPL) 버전 3 또는 그 이후 버전의 조건에 따라 이 프로그램을 재배포하거나 수정할 수 있습니다.
</details>

---

<a name="japanese"></a>
# シェイプキーボーンコントロール作成ツール

<code style="color: #0366d6; background-color: #f6f8fa; padding: 16px; display: block;">
シェイプキーボーンコントロール作成ツールは、シェイプキーをボーンベースのスライダーで視覚化し、制御するBlenderアドオンです。
</code>

<details>
<summary><code style="color: #0366d6; font-size: 1.1em;">✨ 主な機能</code></summary>

- シェイプキーを3Dテキストで視覚化
- スライダーウィジェットによるシェイプキー制御
- メタリグとRigifyリグのサポート
- ボーンベースの制御システム
- ドライバーの自動設定
</details>

<details>
<summary><code style="color: #28a745; font-size: 1.1em;">📥 インストール方法</code></summary>

1. Blenderを起動
2. Edit > Preferences > Add-onsに移動
3. "Install..."をクリック
4. ダウンロードしたZIPファイルを選択
5. アドオンを有効化
</details>

<details>
<summary><code style="color: #5f2eea; font-size: 1.1em;">🎯 使用方法</code></summary>

### 1. 初期設定
- View3D > Sidebar > Shape Key Toolsパネルを開く

### 2. メタリグとRigifyリグの設定
- "Find Metarig"ボタンでメタリグを自動検出
- "Find Rigify"ボタンでRigifyリグを自動検出

### 3. シェイプキーボーンの作成
- "Add Shape Key Bone"ボタンをクリック
- ターゲットメッシュとシェイプキーを選択
- 変形タイプと影響度を設定
- テキストウィジェット作成オプションを選択

### 4. ウィジェット管理
- "Recreate Templates"ボタンでテンプレートをリセット
- "Assign Widget To Bone"ボタンでウィジェットを手動割り当て
</details>

<details>
<summary><code style="color: #6f42c1; font-size: 1.1em;">🔧 機能詳細</code></summary>

### シェイプキーボーン作成
- メタリグに新規ボーンを作成
- Rigifyパラメータの自動設定
- ドライバーの自動接続
- テキストウィジェットの自動生成

### ウィジェットシステム
- ハンドル、スライダー、テキストで構成
- ボーンの動きと連動
- カスタムテキストのサポート

### ドライバーシステム
- 位置、回転、スケールベースの制御
- ユーザー定義の影響度設定
- 自動ドライバー設定
</details>

<details>
<summary><code style="color: #d73a49; font-size: 1.1em;">⚙️ システム要件</code></summary>

- Blender 4.0以上
- Rigifyアドオンが必要
</details>

<details>
<summary><code style="color: #24292e; font-size: 1.1em;">📜 ライセンス</code></summary>

GNU General Public License v3.0 (GPL-3.0)

このプログラムはフリーソフトウェアです。フリーソフトウェア財団によって発行されたGNU 一般公衆利用許諾契約書(GPL)バージョン3または、それ以降のバージョンの条件の下で再配布または改変することができます。
</details>

---

<a name="chinese"></a>
# 形态键骨骼控制创建器

<code style="color: #0366d6; background-color: #f6f8fa; padding: 16px; display: block;">
形态键骨骼控制创建器是一个Blender插件，可以通过基于骨骼的滑块来可视化和控制形态键。
</code>

<details>
<summary><code style="color: #0366d6; font-size: 1.1em;">✨ 主要功能</code></summary>

- 将形态键可视化为3D文本
- 通过滑块部件控制形态键
- 支持元骨架和Rigify骨架
- 基于骨骼的控制系统
- 自动设置驱动器
</details>

<details>
<summary><code style="color: #28a745; font-size: 1.1em;">📥 安装方法</code></summary>

1. 启动Blender
2. 进入Edit > Preferences > Add-ons
3. 点击"Install..."
4. 选择下载的ZIP文件
5. 激活插件
</details>

<details>
<summary><code style="color: #5f2eea; font-size: 1.1em;">🎯 使用方法</code></summary>

### 1. 初始设置
- 找到View3D > Sidebar > Shape Key Tools面板

### 2. 设置元骨架和Rigify骨架
- 点击"Find Metarig"自动检测元骨架
- 点击"Find Rigify"自动检测Rigify骨架

### 3. 创建形态键骨骼
- 点击"Add Shape Key Bone"
- 选择目标网格和形态键
- 设置变换类型和影响度
- 选择文本部件创建选项

### 4. 部件管理
- 点击"Recreate Templates"重置模板
- 点击"Assign Widget To Bone"手动分配部件
</details>

<details>
<summary><code style="color: #6f42c1; font-size: 1.1em;">🔧 功能详情</code></summary>

### 形态键骨骼创建
- 在元骨架中创建新骨骼
- 自动设置Rigify参数
- 自动连接驱动器
- 自动生成文本部件

### 部件系统
- 由手柄、滑块和文本组成
- 与骨骼移动同步
- 支持自定义文本

### 驱动器系统
- 基于位置、旋转、缩放的控制
- 用户自定义影响度设置
- 自动驱动器设置
</details>

<details>
<summary><code style="color: #d73a49; font-size: 1.1em;">⚙️ 系统要求</code></summary>

- Blender 4.0或更高版本
- 需要Rigify插件
</details>

<details>
<summary><code style="color: #24292e; font-size: 1.1em;">📜 许可证</code></summary>

GNU General Public License v3.0 (GPL-3.0)

本程序是自由软件：您可以根据自由软件基金会发布的GNU通用公共许可证的条款重新分发和/或修改它，可以选择使用版本3或更高版本的许可证。
</details>
