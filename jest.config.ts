import type { Config } from 'jest';
import { createJsWithTsPreset } from 'ts-jest';

const compileModules = [
  '@babel',
  '.pnpm',
  // Transform esm to cjs
  'internmap',
  'd3-*',
  'lodash-es',
];

const ignoreList: string[] = [];
const esm = ['internmap', 'd3-*'].join('|');

// cnpm use `_` as prefix
['', '_'].forEach((prefix) => {
  compileModules.forEach((module) => {
    ignoreList.push(`${prefix}${module}`);
  });
});

const transformIgnorePatterns = [
  // Ignore modules without es dir.
  // Update: @babel/runtime should also be transformed
  `<rootDir>/node_modules/(?!(${esm}))`,
  `<rootDir>/node_modules/.pnpm/(?!(${esm}))`,
  // `[/\\\\]node_modules[/\\\\](?!${ignoreList.join('|')})[^/\\\\]+?[/\\\\](?!(es)[/\\\\])`,
];

const config: Config = {
  ...createJsWithTsPreset({
    tsconfig: {
      target: 'ESNext',
      allowJs: true,
    },
  }),
  testEnvironment: 'jsdom',
  collectCoverage: false,
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json'],
  testRegex: '(/__tests__/.*\\.(test|spec))\\.ts$',
  collectCoverageFrom: ['src/**/*.ts'],
  // Transform esm to cjs.
  transformIgnorePatterns,
};

export default config;
