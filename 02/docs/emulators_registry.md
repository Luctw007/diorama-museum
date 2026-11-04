# 模拟器官方档案（emulators_registry.md，人类可读版）

> 本文件由 `tools/index/gen_emulator_doc.py` 从 `emulators_registry.json` 自动生成，手改无效。
> 定位：槽位 manifest 登记母表，供 01 线 slot 系统、05 线 emu-eco、桌面《模拟器清单》三方同源。
> 状态：bone=成熟可接入 / reserved=预留待映射 / researched=调研中。

## fake-slot
- 名称：Fake 后端（本仓库自带）
- 后端类型：native　|　状态：bone　|　后端：已实现
- 模块：gw.emulators.fake_emulator
- 网关登记键：fake　|　槽位 manifest：齐　|　CI 涉及：是
- 目标设备：演示/测试
- 许可：MIT　|　URL：本仓库自带
- 介质类目：cartridge
- 风险：（无）

## mame-apple2
- 名称：MAME（Apple II 驱动）
- 后端类型：mame　|　状态：bone　|　后端：骨架
- 模块：gw.emulators.mame_apple2
- 网关登记键：mame-apple2　|　槽位 manifest：齐　|　CI 涉及：是
- 目标设备：apple-ii
- 许可：GPL-2.0-or-later + BSD-3-Clause　|　URL：https://www.mamedev.org
- 介质类目：disk、tape
- 风险：版本需核实

## mame-handheld
- 名称：MAME（handheld 驱动，Game & Watch）
- 后端类型：mame　|　状态：bone　|　后端：预留
- 网关登记键：（未内置）　|　槽位 manifest：无　|　CI 涉及：否
- 目标设备：game-watch
- 许可：GPL-2.0-or-later（核心 BSD-3）　|　URL：https://www.mamedev.org
- 介质类目：cartridge
- 风险：驱动覆盖机型需核实

## simh-pdp8
- 名称：SIMH（PDP-8）
- 后端类型：simh　|　状态：bone　|　后端：预留
- 网关登记键：simh-pdp8　|　槽位 manifest：齐　|　CI 涉及：是
- 目标设备：pdp8
- 许可：SIMH 自定许可　|　URL：https://simh.trailing-edge.com
- 介质类目：tape、disk
- 风险：许可需核实

## simh-pdp11
- 名称：SIMH（PDP-11）
- 后端类型：simh　|　状态：reserved　|　后端：预留
- 网关登记键：（未内置）　|　槽位 manifest：无　|　CI 涉及：否
- 目标设备：pdp11
- 许可：SIMH 自定许可　|　URL：https://simh.trailing-edge.com
- 介质类目：disk、tape
- 风险：后端模块未实现

## simh-vax11
- 名称：SIMH（VAX-11）
- 后端类型：simh　|　状态：reserved　|　后端：预留
- 网关登记键：（未内置）　|　槽位 manifest：无　|　CI 涉及：否
- 目标设备：vax11
- 许可：SIMH 自定许可　|　URL：https://simh.trailing-edge.com
- 介质类目：disk
- 风险：后端模块未实现

## stella
- 名称：Stella（Atari 2600）
- 后端类型：stella　|　状态：bone　|　后端：预留
- 网关登记键：（未内置）　|　槽位 manifest：无　|　CI 涉及：否
- 目标设备：atari-2600
- 许可：需核实　|　URL：（需核实）
- 介质类目：cartridge
- 风险：许可需核实、后端模块未实现

## mesen
- 名称：Mesen（FC/NES）
- 后端类型：mesen　|　状态：bone　|　后端：预留
- 网关登记键：（未内置）　|　槽位 manifest：无　|　CI 涉及：否
- 目标设备：famicom
- 许可：需核实　|　URL：（需核实）
- 介质类目：cartridge
- 风险：许可需核实、后端模块未实现

## vice
- 名称：VICE（Commodore 64）
- 后端类型：dedicated　|　状态：researched　|　后端：预留
- 网关登记键：（未内置）　|　槽位 manifest：无　|　CI 涉及：否
- 目标设备：commodore64
- 许可：需核实　|　URL：（需核实）
- 介质类目：tape、disk
- 风险：许可需核实、专用后端待模块化

## beebem
- 名称：BeebEm（BBC Micro）
- 后端类型：dedicated　|　状态：researched　|　后端：预留
- 网关登记键：（未内置）　|　槽位 manifest：无　|　CI 涉及：否
- 目标设备：bbcmicro
- 许可：需核实　|　URL：（需核实）
- 介质类目：tape
- 风险：许可需核实、专用后端待模块化

## blastem
- 名称：BlastEm（Sega Mega Drive）
- 后端类型：dedicated　|　状态：researched　|　后端：预留
- 网关登记键：（未内置）　|　槽位 manifest：无　|　CI 涉及：否
- 目标设备：sega-md
- 许可：需核实　|　URL：（需核实）
- 介质类目：cartridge
- 风险：许可需核实、专用后端待模块化

## pc86box
- 名称：PC-86box（IBM PC 5150）
- 后端类型：dedicated　|　状态：researched　|　后端：预留
- 网关登记键：（未内置）　|　槽位 manifest：无　|　CI 涉及：否
- 目标设备：ibm5150
- 许可：需核实　|　URL：（需核实）
- 介质类目：disk
- 风险：许可需核实、专用后端待模块化

## qedsac
- 名称：QEDSAC（EDSAC）
- 后端类型：dedicated　|　状态：researched　|　后端：预留
- 网关登记键：（未内置）　|　槽位 manifest：无　|　CI 涉及：否
- 目标设备：edsac
- 许可：需核实　|　URL：（需核实）
- 介质类目：tape
- 风险：许可需核实

## davidpsharp-baby
- 名称：David PSharp Baby（Manchester Baby）
- 后端类型：dedicated　|　状态：researched　|　后端：预留
- 网关登记键：（未内置）　|　槽位 manifest：无　|　CI 涉及：否
- 目标设备：manchester-baby
- 许可：需核实　|　URL：（需核实）
- 介质类目：（无）
- 风险：许可需核实

## sameboy
- 名称：SameBoy（Game Boy）
- 后端类型：dedicated　|　状态：researched　|　后端：预留
- 网关登记键：（未内置）　|　槽位 manifest：无　|　CI 涉及：否
- 目标设备：game-boy
- 许可：需核实　|　URL：（需核实）
- 介质类目：cartridge
- 风险：许可需核实、专用后端待模块化

## eka2l1
- 名称：EKA2L1（Symbian OS / Nokia N-Gage / S60）
- 后端类型：mobile　|　状态：bone　|　后端：预留
- 网关登记键：（未内置）　|　槽位 manifest：无　|　CI 涉及：否
- 目标设备：symbian、n-gage
- 许可：GPL-3.0　|　URL：https://github.com/EKA2L1/EKA2L1
- 介质类目：firmware、app_package
- 风险：无 headless 接口（需核实）、需真机固件（介质红线）

## cloudpilotemu
- 名称：CloudpilotEmu（Palm OS）
- 后端类型：mobile　|　状态：bone　|　后端：预留
- 网关登记键：（未内置）　|　槽位 manifest：无　|　CI 涉及：否
- 目标设备：palm-os
- 许可：GPL-3.0　|　URL：https://github.com/cloudpilot-emu/cloudpilot-emu
- 介质类目：firmware
- 风险：需 ROM（介质红线）、CLI/GDB stub 接入需 spike

## madrigal
- 名称：MADrigal Game & Watch Simulators（网页）
- 后端类型：dedicated　|　状态：researched　|　后端：预留
- 网关登记键：（未内置）　|　槽位 manifest：无　|　CI 涉及：否
- 目标设备：game-watch
- 许可：需核实　|　URL：https://www.madrigaldesign.it/sim/
- 介质类目：cartridge
- 风险：许可需核实、网页 sim（JS），非网关后端

## qemu
- 名称：QEMU（iPhone OS 实验）
- 后端类型：dedicated　|　状态：reserved　|　后端：预留
- 网关登记键：（未内置）　|　槽位 manifest：无　|　CI 涉及：否
- 目标设备：iphone-os-早期
- 许可：需核实　|　URL：（需核实）
- 介质类目：firmware
- 风险：实验性，不可运行应用（需核实）

## system360-emulator
- 名称：System/360 模拟器（待定）
- 后端类型：dedicated　|　状态：reserved　|　后端：预留
- 网关登记键：（未内置）　|　槽位 manifest：无　|　CI 涉及：否
- 目标设备：system360
- 许可：需核实　|　URL：（需核实）
- 介质类目：tape
- 风险：后端待定

## hercules
- 名称：Hercules (IBM System/360)
- 后端类型：dedicated　|　状态：reserved　|　后端：预留
- 网关登记键：（未内置）　|　槽位 manifest：无　|　CI 涉及：否
- 目标设备：system360
- 许可：QPL 例外条款　|　URL：（需核实）
- 介质类目：disk、tape
- 风险：许可需核实、后端模块未实现

## 86box
- 名称：86Box / PCem (IBM PC 5150)
- 后端类型：dedicated　|　状态：researched　|　后端：预留
- 网关登记键：（未内置）　|　槽位 manifest：无　|　CI 涉及：否
- 目标设备：ibm5150
- 许可：GPL-2.0　|　URL：（需核实）
- 介质类目：disk
- 风险：许可需核实

## mini-vmac
- 名称：Mini vMac (Macintosh 128K)
- 后端类型：dedicated　|　状态：reserved　|　后端：预留
- 网关登记键：（未内置）　|　槽位 manifest：无　|　CI 涉及：否
- 目标设备：macintosh128k
- 许可：GPL-2.0　|　URL：（需核实）
- 介质类目：disk
- 风险：许可需核实

## fuse
- 名称：Fuse (ZX Spectrum)
- 后端类型：dedicated　|　状态：reserved　|　后端：预留
- 网关登记键：（未内置）　|　槽位 manifest：无　|　CI 涉及：否
- 目标设备：zx-spectrum
- 许可：GPL-2.0　|　URL：（需核实）
- 介质类目：tape
- 风险：许可需核实

## snes9x
- 名称：Snes9x / Mesen (SFC)
- 后端类型：dedicated　|　状态：reserved　|　后端：预留
- 网关登记键：（未内置）　|　槽位 manifest：无　|　CI 涉及：否
- 目标设备：sfc
- 许可：Snes9x 非商业条款　|　URL：（需核实）
- 介质类目：cartridge
- 风险：许可需核实

## mame-neogeo
- 名称：MAME neogeo 驱动 (Neo Geo MVS)
- 后端类型：mame　|　状态：reserved　|　后端：预留
- 网关登记键：（未内置）　|　槽位 manifest：无　|　CI 涉及：否
- 目标设备：neo-geo-mvs
- 许可：GPL-2.0-or-later + BSD-3-Clause　|　URL：https://www.mamedev.org
- 介质类目：cartridge
- 风险：版本需核实

