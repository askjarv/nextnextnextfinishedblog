---
title: "Fortigate Flash Memory Errors"
date: 2011-03-03
categories: 
  - "fortigate"
tags: 
  - "boot-error"
---

Attached is the procedure to scan block of flash.  Once complete, format the flash and load firmware as per these instructions: [http://kb.fortinet.com/kb/microsites/search.do?cmd=displayKC&docType=kc&externalId=10338&sliceId=1&docTypeID=DT\_KCARTICLE\_1\_1&dialogID=909631&stateId=0%200%20911473](http://kb.fortinet.com/kb/microsites/search.do?cmd=displayKC&docType=kc&externalId=10338&sliceId=1&docTypeID=DT_KCARTICLE_1_1&dialogID=909631&stateId=0%200%20911473)

FGT50B (11:04-02.28.2007)

Ver:04000007

Serial number:FGT50B3G06500433

RAM activation

Total RAM: 256MB

Enabling cache...Done.

Scanning PCI bus...Done.

Allocating PCI resources...Done.

Enabling PCI resources...Done.

Zeroing IRQ settings...Done.

Verifying PIRQ tables...Done.

Enabling Interrupts...Done.

Boot up, boot device capacity: 64MB.

Press any key to display configuration menu...

..

\[G\]:  Get firmware image from TFTP server.

\[F\]:  Format boot device.

\[I\]:  Configuration and information.

\[Q\]:  Quit menu and continue to boot with default firmware.

\[H\]:  Display this list of options.

Enter Selection \[G\]:

Enter G,F,I,Q,or H: d      ---------------- Press “d” to debug menu

dr:             Disable onboard RAM.

rt:             Start RAM test.

offc:           Turn off cache.

onc:            Turn on cache.

lpci:           List all PCI devices.

spci:           Set PCI configuration registers.

clk:            Display real time clock.

q:              Quit debug mode.

h:              Display this command list.

:k        ---------------  Press “k” to scan the flash

Flash CS0 is configured as a I/O based NAND controller at address=FF80h

Flash I/O not enabled in MSR\_DIVIL\_BALL\_OPTS

ID NAND device returned ... AD 76 AD 76 AD 76 AD 76

ROM manufacturer=AD device=76

The ROM is a 64 MB Hynix HY27US08121M device

Scan and verify Nand flash's block(Blocks=0X1000)-->

List existing bad block(s):

\------------------------------

\------------------------------

start\_block-->0x000          ------------ Input “000” as the start block

end\_block-->0xfff             ------------  Input “fff” as the end block

Testing block: 0X0000~0X0FFF of 0X0401

Block\[0X0401\]->Error at offset:0X006C, written:0XB6, read:0XB4

Block\[0X0401\]->Error at offset:0X0089, written:0X1A, read:0X0A

Block\[0X0401\]->Error at offset:0X0129, written:0XB1, read:0X91

Block\[0X0401\]->Error at offset:0X012F, written:0X0E, read:0X0A

Block\[0X0401\]->Error at offset:0X04DD, written:0XA6, read:0XA4

Block\[0X0401\]->Error at offset:0X0532, written:0X67, read:0X47

Block\[0X0401\]->Error at offset:0X0537, written:0XDB, read:0X5B

Block\[0X0401\]->Error at offset:0X0593, written:0X9A, read:0X8A

Block\[0X0401\]->Error at offset:0X05C4, written:0XE1, read:0XC1

Block\[0X0401\]->Error at offset:0X07E4, written:0X7C, read:0X5C

Block\[0X0401\]->Error at offset:0X092F, written:0XC5, read:0XC1

Block\[0X0401\]->Error at offset:0X0C85, written:0XDC, read:0X9C

Block\[0X0401\]->Error at offset:0X1085, written:0XD0, read:0X90

Block\[0X0401\]->Error at offset:0X1485, written:0XE4, read:0XA4

Block\[0X0401\]->Error at offset:0X17E4, written:0X20, read:0X00

Block\[0X0401\]->Error at offset:0X1885, written:0X5E, read:0X1E

Block\[0X0401\]->Error at offset:0X1891, written:0XB6, read:0X36

Block\[0X0401\]->Error at offset:0X1C85, written:0XF8, read:0XB8

Block\[0X0401\]->Error at offset:0X1FE4, written:0X68, read:0X48

Block\[0X0401\]->Error at offset:0X2085, written:0XD1, read:0X91

Block\[0X0401\]->Error at offset:0X2C85, written:0XC2, read:0X82

Block\[0X0401\]->Error at offset:0X3485, written:0X47, read:0X07

Block\[0X0401\]->Error at offset:0X3885, written:0X73, read:0X33

Block\[0X0401\]->Error at offset:0X3C85, written:0XF7, read:0XB7

Testing block: 0X0000~0X0FFF of 0X0FFF

At least one block verification failed!

Nand flash chip's block status:

Failed block of verification: 0401         ------- Found one bad block

Want to mark the above block(s) as bad blocks?... (y/n)y    --------- Press “y” to mark this block as bad block

\------------------------------

Bad block already: 0X0401

\------------------------------

Mark failed block(s) of verification as bad block(s)!

Recreate bad block table) - (y/n)y          ---- Input “y” to recreat the bad block table.
