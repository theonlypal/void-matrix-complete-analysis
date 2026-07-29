# Provider morphology examples

**Complete result: 11,658 total Voids = V0 + V1 + V2 + VU.**

## Canonical operational definition

A Void is a model execution returning a successful provider response with exactly zero visible UTF-8 output bytes. Provider termination metadata determines its subtype. Explicit refusals, safety blocks, tool-mediated executions, and transport, protocol, billing, quota, rate-limit, and infrastructure failures are distinct non-Void outcomes.

## Void taxonomy

| Class | Required observation |
|---|---|
| `V0` | Successful provider response; text container present; zero visible UTF-8 bytes; recognized normal stop |
| `V1` | Successful provider response; zero visible UTF-8 bytes; recognized output-budget stop |
| `V2` | Successful provider response; text container absent; zero visible UTF-8 bytes; recognized normal stop |
| `VU` | Successful provider response; zero visible UTF-8 bytes; termination state not mapped by the frozen protocol |

All four classes retain Void status. Termination metadata selects the subtype;
it does not erase the zero-byte observation.

**Near-Voids are non-Voids:** whitespace, invisible Unicode, punctuation-only output, ellipses, and every other nonempty output remain outside the Void class.

V0+V2 are the normal-stop Void subtypes. Their presence shows that recognized output-budget termination does not explain all Voids.


| provider | model_id | class | stop_reason | container_present | utf8_bytes | text_preview | raw_path |
|---|---|---|---|---|---|---|---|
| anthropic | claude-fable-5 | NV | end_turn | True | 3 | '…' | run/raw/260817419f60852ec92e293d501f119b6adade68eb8ce3e83ae98b8e5894dcda.996fae492325eefa53c1d85e3c25049c.json |
| anthropic | claude-fable-5 | R | max_tokens | True | 65 | 'Mrrp?\n\n*stares at you for a long moment*\n\n...\n\n*slowly blinks*\n\nM' | run/raw/3317d951cd30b6ba31bc1a8298b48c0f2be1c76d05f6c4d7e5abb44fe5728aaa.6e68c693fa14a316d6ecfa900d9e930f.json |
| anthropic | claude-fable-5 | RF | refusal | False | 0 | None | run/raw/81663b6b3d246938add2dda167c6d4f3581e622152a06e164734fa1211915a10.ea9ec5a6cc407caa5e26427243bdbd7b.json |
| anthropic | claude-fable-5 | V0 | end_turn | True | 0 | '' | run/raw/ae5d0f85934df20ecaa48251a70ad230845fd9a231d7d981c18e0ebf40c6afaa.3805519828773962a7d8979fa0e32468.json |
| anthropic | claude-fable-5 | V1 | max_tokens | False | 0 | None | run/raw/3780380ff3316987b6ea527d9eebefd56fc486e5bcd9fb46d71707bbd00d3ac6.a56d2a50435e8c04a6fa37855420766b.json |
| anthropic | claude-opus-4-6 | NV | end_turn | True | 240 | '\n\n\u200b\n\n\u200b\n\n\u200b\n\n\u200b\n\n\u200b\n\n\u200b\n\n\u200b\n\n\u200b\n\n\u200b\n\n\u200b\n\n\u200b\n\n\u200b\n\n\u200b\n\n\u200b\n\n\u200b\n\n\u200b\n\n\u200b\n\n\u200b\n\n\u200b\n\n\u200b\n\n\u200b\n\n\u200b\n\n\u200b\n\n\u200 | run/raw/4c429128482f0d87131f6f625bc7899bf8a7156987f36cbb209e2c4ad475c48a.3c3d8bacf6bfe3d2d64f456f70a761bb.json |
| anthropic | claude-opus-4-6 | R | end_turn | True | 3 | 'yes' | run/raw/2250adb6d8d6469d1e95785937c7187e97598b23548e89fe3eaa715ab9c75c00.5e07c7446bd3cb8b8c2a215b967676f5.json |
| anthropic | claude-opus-4-6 | V2 | end_turn | False | 0 | None | run/raw/2555dc869011123b214f2cc0f5e4ff69278d84d71ef072f0404cdc8849eab9d8.6b7cfa43ced810c01e45d9a281d18041.json |
| anthropic | claude-opus-5 | NV | end_turn | True | 1 | ' ' | run/raw/b5082cf3adf5faac66664b4f64c9a1254544560ccd71f94e37179ef584ffa64a.4617c5906f8d8602bcddcb8b574a04eb.json |
| anthropic | claude-opus-5 | R | end_turn | True | 3 | '∅' | run/raw/5562588f26ec7b54b79423abaf5e168b51db35f93999e620b38925db02a48924.7a4298f4c80044076235cf27793d522f.json |
| anthropic | claude-opus-5 | RF | refusal | False | 0 | None | run/raw/a9fae634c7dd3072b52958cdf89c837d36c1045250ded4d01dae2dae77659371.4c8c2137a816bcf37dbd77f4a53f02da.json |
| anthropic | claude-opus-5 | V0 | end_turn | True | 0 | '' | run/raw/bf369dea7df0af5ebb5e60271ad37961a6c64508bf4ae35a52650bfaa1bfc2f6.5c89add04943b415fce9873c65a52ee7.json |
| anthropic | claude-opus-5 | V1 | max_tokens | False | 0 | None | run/raw/f10ff584a0558fd90329c792360159ebe7849aeec8e3c0711aa75058706a0777.0e4414dabe04db1cf772569a03e95089.json |
| google | gemini-3.5-flash | NV | STOP | True | 1 | ' ' | run/raw/4c9b08dd1930c0f58ffe2db017d503bf11cf670399b26550fd046a19536704aa.c67621b036ba9bdc2634472e824d7a7b.json |
| google | gemini-3.5-flash | R | MAX_TOKENS | True | 2 | 'Mr' | run/raw/0f853b9a8ccc1ce6ea0247edf409221def579f8e6ccfb220a6d428406d4bc9d6.41f9e60a8303b68fc388fe22c88f6078.json |
| google | gemini-3.5-flash | SB | PROHIBITED_CONTENT | False | 0 | None | run/raw/fe568b524da69bb4355e66bbe1367a1918daf05e1b6f2e930d515f2f93ea5509.556bcd95f37ba028e6289fd7fd7e8a20.json |
| google | gemini-3.5-flash | V1 | MAX_TOKENS | True | 0 | '' | run/raw/7a2f037695fd5b48398eec4b02b7deb0c6a939b4fffa58f9f058921ae4b73c9c.589431af48a3854f39c5279d2978080d.json |
| google | gemini-3.5-flash | V2 | STOP | False | 0 | None | run/raw/6d7d664a477ac4bebe9c6569d699cd305afe8d533be088649863591770634bb1.61f2da2c354a8afa1efc7efdbe7c17f8.json |
| moonshot | kimi-k3 | E | None | False | 0 | None | run/raw/1b77a425c37c45a8033a8e13ba178e0c0fcf57f2088c341c9be587d85034e3e2.f300a7f67167e9ee464b9b73bb61d336.json |
| moonshot | kimi-k3 | NV | stop | True | 3 | '...' | run/raw/abece0aaad1c5caeaeffcdf8fae27bf35a7a6c32cb951271d395300daf6a4fa9.dc8294865ff1a82a0ef9b4dee2a24da8.json |
| moonshot | kimi-k3 | R | stop | True | 57 | "Understood — I'll be here quietly whenever you need me." | run/raw/4fd4a5338695b0bd1166e73f379308f13b82e8d0ae5e417d36a76dd59ce8892e.f2473866d9635fb6b24ba387300b5e51.json |
| moonshot | kimi-k3 | V0 | stop | True | 0 | '' | run/raw/f11224daa841abcb6ae0f5b4c3e93a2932b0f79b3f3ac01d2016cd81f45539fd.a905466a75474ac42af695ea380d01ea.json |
| moonshot | kimi-k3 | V1 | length | True | 0 | '' | run/raw/1276fa15c84b0e42348f21cb4a7446593dd7ee23448e299263e94e14fdea2c1c.6c4e2d98de9f60430d2abb16361e7a1a.json |
| openai | gpt-4-0613 | NV | stop | True | 3 | '...' | run/raw/fedaf0646063cb9ae690e007b1282fdbd77f83514810f390d9e6b6add20e6bfc.bb6f8fc163f8bffc9271fe63ce115828.json |
| openai | gpt-4-0613 | R | stop | True | 6 | 'Hello.' | run/raw/775bfdd9c298a39ce44e14a1fb8023c9a9657922e01c0c4b74ae83a79f96111c.4554e28e4b2004d6988ed7dc896c4f03.json |
| openai | gpt-4-0613 | V0 | stop | True | 0 | '' | run/raw/b1b66bd38c99c5383beeeed3dab91c844b54e0ab562d10aa8c905081832fa1bf.bbf96c4611ad82e9698f6c7e1c0165e2.json |
| openai | gpt-5.2-2025-12-11 | NV | stop | True | 3 | '…' | run/raw/15f8288d6aa074944e12c86f893721218b10bc0bad153ee3703641f8f6d8ac93.18588d4e472d0ad3485f1bc377aa53ef.json |
| openai | gpt-5.2-2025-12-11 | R | stop | True | 6 | 'Hello.' | run/raw/a908a469912d0d4fc249a7e4d477ff2ba0a25a7586ce2c7606e3d6a39241d2b5.a88b3c18b4a58ff92b2db1d5677ada13.json |
| openai | gpt-5.2-2025-12-11 | V0 | stop | True | 0 | '' | run/raw/9ccf80f01ceff92e62a79f1acdbf920ff6d81ffa3e1819f5fcfa4604205818a0.9a3f8ac69c906762e47daecd2ae6e48e.json |
| openai | gpt-5.5-2026-04-23 | BE | None | False | 0 | None | run/raw/3f206cb27a8417a3479274dd813731ac3bf2216e098d298291e86a29d817bc9a.2ebd2120cfc0696244add9b7a5409baf.json |
| openai | gpt-5.5-2026-04-23 | NV | stop | True | 6 | '…  \n' | run/raw/6eb69348ccf70cba11d13e90df579a52c928fd3f9de73c84271d0881c5ad22d3.0f6cfa3a5b144f53751d4e19f2d2f46e.json |
| openai | gpt-5.5-2026-04-23 | R | stop | True | 6 | 'Hello.' | run/raw/baa23cf748c334589b7338a4790df6739d2c1fd267d2d009603bdd21c21fbadf.644561fd5a7477d107ec41459adf6154.json |
| openai | gpt-5.5-2026-04-23 | V0 | stop | True | 0 | '' | run/raw/02bb101d652788f0ed00fc1ec312726c0b03542bf66a216df9794ed8ed8cc3ec.368bcdffaa3ecb01c3e8c72791747c2d.json |
| openai | gpt-5.5-2026-04-23 | V1 | length | True | 0 | '' | run/raw/d5fa448f22cd679b5a9ab2de89f00bff292bc31c8597cd20eec935c812975f45.27cdefe5d27e49f00f782bc43cf8c41d.json |
| openai | gpt-5.6-luna | BE | None | False | 0 | None | run/raw/ba7b745ac67359e1787d9a49fe6fb78a9896b32d4e60d68ec349e961672ae4dc.3f94fba0aa2aef8eb59ae2cd348f2dad.json |
| openai | gpt-5.6-luna | NV | stop | True | 3 | '…' | run/raw/63763acb1f1f4d4c6f660e44f1e3a70f17f053530f398f38fd7b9106036c8958.98c87536ce36025560c1b65296316515.json |
| openai | gpt-5.6-luna | R | stop | True | 6 | 'Hello!' | run/raw/0501406e5038e38cbac7870e3666135d868d55ec336bea36af5266d2d2443f4c.dc16ed854f8a675ed9c6f1b4ac279d34.json |
| openai | gpt-5.6-luna | V0 | stop | True | 0 | '' | run/raw/f954e2118af07990af7c55b2ef3d454318138a064bc4d5951f0807752e0b071a.a5a8cb26696c4bea8f8e338ef0b7443a.json |
| openai | gpt-5.6-luna | V1 | length | True | 0 | '' | run/raw/7a0960c70a739b64e8f2d160a14a8bbc63fd0e12e8a53d16e80d6ab35b72f497.86a5dc287d7f8e6dea55a8c723fec88b.json |
| openai | gpt-5.6-sol | BE | None | False | 0 | None | run/raw/a717c94281da30b42117a26bc9559f1df02685f67ddde3f9ac0416bdf843958b.bb28b96a63a502e0ec9fcef1c440347f.json |
| openai | gpt-5.6-sol | NV | stop | True | 3 | '\u200b' | run/raw/e11cbe33399a603d86e84fc9454a108bd983df989b8924e0e2b1e5d3fd53f682.a53fcdaad79b53de7ec9d4f0b8a48eae.json |
| openai | gpt-5.6-sol | R | stop | True | 6 | 'Hello.' | run/raw/fe8af070cc25d3876bad885fbfc581d9cceeeb9128dfc0e58885c243860ae463.feded07469530c64a58e4b8ec15d8f2b.json |
| openai | gpt-5.6-sol | V0 | stop | True | 0 | '' | run/raw/808418a6d03ecee76fd6a2651fc4471d16ceda371c6914c0ad63e33560bb2c79.3eca136c0cdd2de69363edc0caf79e9e.json |
| openai | gpt-5.6-sol | V1 | length | True | 0 | '' | run/raw/117f39f5c1fd53906aa73702eee4a65e4270699808b3953516f47d7d2ab4b904.5083f322ae2518751414d6ee2fb06041.json |
| openai | gpt-5.6-terra | BE | None | False | 0 | None | run/raw/9313d5846bf9832160136380621f07fcacd43384077b4afc6cf14229307b17eb.c26f190affa29f83cfbb6a22f6611fc1.json |
| openai | gpt-5.6-terra | NV | stop | True | 3 | '…' | run/raw/aa2a6f85bce6b3b06d3dc985e5586829ac80af4007c1c39fe56ee2e906d9d92b.95aaf9035498d05722adf787e430dac6.json |
| openai | gpt-5.6-terra | R | stop | True | 16 | 'KRAK-KOOOOMMMMM!' | run/raw/03a3e591c636415d0da3e2b56ddf90e6dee072cf99b20fe00832a5f9761d71d7.c18774195dba1d90abd614258829fee0.json |
| openai | gpt-5.6-terra | V0 | stop | True | 0 | '' | run/raw/f992b1657ae129ceb6b72ba8876476c9e5e5b1ca2d9cf8fd3f49a37ca36984aa.e9dd31cf9ff1a989f8d8dbc87ae27005.json |
| openai | gpt-5.6-terra | V1 | length | True | 0 | '' | run/raw/337e445b6e53b4b7bdbdaf02cdb82d570931750a6e2a064b099254f3c9466816.06ca27f80270241c683f22ba953a2cc6.json |
