import { execFileSync } from "node:child_process";
import { writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import openapiTS, { astToString } from "openapi-typescript";

const backendDir = fileURLToPath(new URL("../../backend", import.meta.url));
const outFile = fileURLToPath(new URL("../src/types/api.d.ts", import.meta.url));

const dumpSchema = `
import json, sys
sys.path.insert(0, "src")
from main import app
print(json.dumps(app.openapi()))
`;

const schemaJson = execFileSync("uv", ["run", "python", "-c", dumpSchema], {
  cwd: backendDir,
  encoding: "utf-8",
});

const ast = await openapiTS(JSON.parse(schemaJson));
writeFileSync(outFile, astToString(ast));

console.log(`generated ${outFile}`);
