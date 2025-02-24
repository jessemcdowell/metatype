// Copyright Metatype OÜ, licensed under the Elastic License 2.0.
// SPDX-License-Identifier: Elastic-2.0

import { Typegate } from "../typegate/mod.ts";
import { PythonWasiRuntime } from "./python_wasi/python_wasi.ts";

Typegate.registerRuntime("python_wasi", PythonWasiRuntime.init);
