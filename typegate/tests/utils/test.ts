// Copyright Metatype OÜ, licensed under the Elastic License 2.0.
// SPDX-License-Identifier: Elastic-2.0

import { SystemTypegraph } from "../../src/system_typegraphs.ts";
import { MemoryRegister } from "./memory_register.ts";
import { join } from "std/path/mod.ts";
import { testDir } from "./dir.ts";
import { shell } from "./shell.ts";

import { Server } from "std/http/server.ts";
import { assertSnapshot } from "std/testing/snapshot.ts";
import { assertEquals, assertNotEquals } from "std/testing/asserts.ts";
import { Engine } from "../../src/engine.ts";
import { Typegate } from "../../src/typegate/mod.ts";
import { ConnInfo } from "std/http/server.ts";

import { NoLimiter } from "./no_limiter.ts";
import { SingleRegister } from "./single_register.ts";
import { meta } from "./meta.ts";

type AssertSnapshotParams = typeof assertSnapshot extends (
  ctx: Deno.TestContext,
  ...rest: infer R
) => Promise<void> ? R
  : never;

export interface ParseOptions {
  deploy?: boolean;
  typegraph?: string;
  // ports on which this typegraph will be exposed
  ports?: number[];
  secrets?: Record<string, string>;
  prefix?: string;
  pretty?: boolean;
}

function serve(typegate: Typegate, port: number): () => void {
  const server = new Server({
    port,
    hostname: "localhost",
    handler(req) {
      return typegate.handle(req, {
        remoteAddr: { hostname: "localhost" },
      } as ConnInfo);
    },
  });

  const listener = server.listenAndServe();
  return async () => {
    server.close();
    await listener;
  };
}

function exposeOnPort(engine: Engine, port: number): () => void {
  const register = new SingleRegister(engine.name, engine);
  return serve(new Typegate(register, new NoLimiter()), port);
}

type MetaTestCleanupFn = () => void | Promise<void>;

export class MetaTest {
  private cleanups: MetaTestCleanupFn[] = [];

  constructor(
    public t: Deno.TestContext,
    public typegate: Typegate,
    private introspection: boolean,
    port: number | null,
  ) {
    if (port != null) {
      this.cleanups.push(serve(typegate, port));
    }
  }

  private get register() {
    return this.typegate.register;
  }

  addCleanup(fn: MetaTestCleanupFn) {
    this.cleanups.push(fn);
  }

  getTypegraph(name: string, ports: number[] = []): Engine | undefined {
    const engine = this.register.get(name);
    if (engine != null) {
      this.cleanups.push(...ports.map((port) => exposeOnPort(engine, port)));
    }
    return engine;
  }

  async serialize(path: string, opts: ParseOptions = {}): Promise<string> {
    const { deploy = false, typegraph = null, prefix = null, pretty = false } =
      opts;
    const cmd = ["serialize", "-f", path];

    if (pretty) {
      cmd.push("--pretty");
    }

    if (prefix != null) {
      cmd.push("--prefix", prefix);
    }

    if (typegraph == null) {
      cmd.push("-1");
    } else {
      cmd.push("--typegraph", typegraph);
    }

    if (deploy) {
      cmd.push("--deploy");
    }

    const stdout = await meta(...cmd);
    if (stdout.length == 0) {
      throw new Error("No typegraph");
    }

    return stdout;
  }

  async engine(path: string, opts: ParseOptions = {}): Promise<Engine> {
    const tgJson = await this.serialize(path, opts);
    const [engine, _] = await this.typegate.pushTypegraph(
      tgJson,
      opts.secrets ?? {},
      this.introspection,
    );

    this.cleanups.push(
      ...(opts.ports ?? []).map((port) => exposeOnPort(engine, port)),
    );

    return engine;
  }

  async unregister(engine: Engine) {
    await Promise.all(
      this.register
        .list()
        .filter((e) => e == engine)
        .map((e) => {
          this.register.remove(e.name);
          return e.terminate();
        }),
    );
  }

  async terminate() {
    await Promise.all(this.cleanups.map((c) => c()));
    await Promise.all(
      this.register.list().map((e) => e.terminate()),
    );
  }

  async should(
    fact: string,
    fn: (t: Deno.TestContext) => void | Promise<void>,
  ): Promise<boolean> {
    const res = await this.t.step({
      name: `should ${fact}`,
      fn: async (t) => {
        try {
          await fn(t);
        } catch (e) {
          console.error(e);
          throw e;
        }
      },
    });
    if (!res) {
      console.error(`step ${fact} failed unexpectedly`);
    }

    return true;
  }

  async assertSnapshot(...params: AssertSnapshotParams): Promise<void> {
    await assertSnapshot(this.t, ...params);
  }

  async assertThrowsSnapshot(fn: () => void): Promise<void> {
    let err: Error | null = null;
    try {
      fn();
    } catch (e) {
      err = e;
    }

    if (err == null) {
      throw new Error("Assertion failure: function did not throw");
    }
    await this.assertSnapshot(err.message);
  }

  async assertSameTypegraphs(...paths: string[]) {
    assertNotEquals(paths.length, 0);
    const first = paths.shift()!;
    const expected = await this.serialize(first, { pretty: true });
    for (const path of paths) {
      await this.should(
        `serialize ${path} to the same typegraph as ${first}`,
        async () => {
          const actual = await this.serialize(path, { pretty: true });
          assertEquals(actual, expected);
        },
      );
    }
  }
}

interface TestConfig {
  systemTypegraphs?: boolean;
  introspection?: boolean;
  // port on which the typegate instance will be exposed on expose the typegate instance
  port?: number;
  // create a temporary clean git repo for the tests
  cleanGitRepo?: boolean;
}

interface Test {
  (
    name: string,
    fn: (t: MetaTest) => void | Promise<void>,
    opts?: Omit<Deno.TestDefinition, "name" | "fn"> & TestConfig,
  ): void;
}

interface TestExt extends Test {
  only: Test;
  ignore: Test;
}

export const test = ((name, fn, opts = {}): void => {
  return Deno.test({
    name,
    async fn(t) {
      const typegate = new Typegate(new MemoryRegister(), new NoLimiter());
      const {
        systemTypegraphs = false,
        cleanGitRepo = false,
        introspection = false,
      } = opts;
      if (systemTypegraphs) {
        await SystemTypegraph.loadAll(typegate);
      }

      const mt = new MetaTest(t, typegate, introspection, opts.port ?? null);

      try {
        if (cleanGitRepo) {
          await Deno.remove(join(testDir, ".git"), { recursive: true }).catch(
            () => {},
          );
          await shell(["git", "init"]);
          await shell(["git", "config", "user.name", "user"]);
          await shell(["git", "config", "user.email", "user@example.com"]);
          await shell(["git", "add", "."]);
          await shell(["git", "commit", "-m", "Initial commit"]);
          mt.addCleanup(() =>
            Deno.remove(join(testDir, ".git"), { recursive: true })
          );
        }

        await fn(mt);
      } catch (error) {
        console.error(error);
        throw error;
      } finally {
        await mt.terminate();
      }
    },
    ...opts,
  });
}) as TestExt;

test.only = (name, fn, opts = {}) => test(name, fn, { ...opts, only: true });

test.ignore = (name, fn, opts = {}) =>
  test(name, fn, { ...opts, ignore: true });
