
external_libraries = ["--disable%s" % p for p in ("-avs",
                                            "-swscale",
                                            "-lavf",
                                            "-ffms",
                                            "-gpac",
                                            "-lsmash"
                                            )]

advanced_options = ["--enable%s" % p for p in ("-lto", 
                                            "-debug", 
                                            "-gprof",
                                            "-strip",
                                            "-pic"
                                            ) ]
advanced_options_2 = ["--disable-asm"]

configuration_options = ["--enable%s" % p for p in ("-shared", 
                                            "-static", 
                                            "-bashcompletion"
                                            ) ]
configuration_options_2 = ["--disable%s" % p for p in ("-bashcompletion", 
                                            "-opencl", 
                                            "-gpl",
                                            "-thread",
                                            "-win32thread",
                                            "-interlaced"
                                            ) ]
configuration_options_3 = ["--system-libx264"]

configuration_options_4 = ["--bit-depth=%s" % p for p in ("8", 
                                            "10", 
                                            "all"
                                            ) ]

configuration_options_5 = ["--chroma-format=%s" % p for p in ("400", 
                                            "420", 
                                            "422",
                                            "444",
                                            "all"
                                            ) ]

all_options = []
all_options = [*external_libraries, *advanced_options, *advanced_options_2, 
                *configuration_options, *configuration_options_2, *configuration_options_3,
                *configuration_options_4, *configuration_options_5] 