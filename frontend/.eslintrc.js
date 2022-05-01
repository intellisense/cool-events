module.exports = {
  root: true,
  env: {
    browser: true,
    node: true,
  },
  parserOptions: {
    sourceType: 'module',
    parser: '@babel/eslint-parser',
  },
  extends: [
    'airbnb-base',
    'plugin:vue/essential',
    'plugin:vue/recommended',
  ],
  plugins: ['import', 'vue'],
  rules: {
    'no-shadow': ['error', { allow: ['state'] }],
    'no-param-reassign': ['error', { props: false }],
    'import/extensions': ['error', 'ignorePackages', {
      js: 'never',
      mjs: 'never',
      jsx: 'never',
      ts: 'never',
      tsx: 'never',
      vue: 'never',
    }],
    'vue/multi-word-component-names': 'off',
    'no-underscore-dangle': ['error', { allow: ['_types'] }],
  },
  settings: {
    'import/resolver': {
      node: {
        extensions: ['.js', '.jsx', '.ts', '.tsx', '.vue'],
      },
      'babel-module': {}, // Use babel module resolver
    },
    'import/extensions': ['.js', '.jsx', '.ts', '.tsx', '.vue'],
  },
};
