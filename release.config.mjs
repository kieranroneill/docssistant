/**
 * @type {import('semantic-release').GlobalConfig}
 */
export default {
  branches: [
    'main',
    {
      name: 'beta',
      prerelease: true,
    },
  ],
  plugins: [
    '@semantic-release/commit-analyzer',
    '@semantic-release/release-notes-generator',
    '@semantic-release/changelog',
    ['@semantic-release/npm', { npmPublish: false }],
    [
      '@semantic-release/exec',
      {
        prepareCmd: 'pnpm tsx ./scripts/update-pyproject-version.ts ${nextRelease.version}',
      },
    ],
    [
      '@semantic-release/git',
      {
        assets: ['package.json', 'pyproject.toml', 'CHANGELOG.md'],
        message: 'chore(release): ${nextRelease.version}\n\n${nextRelease.notes}',
      },
    ],
    [
      '@semantic-release/github',
      {
        releasedLabels: ['🚀 released'],
      },
    ],
  ],
};
