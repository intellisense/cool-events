const path = require('path');
const { defineConfig } = require('@vue/cli-service');
const BundleTracker = require('webpack-bundle-tracker');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');

const host = '0.0.0.0';
const port = 8080;

module.exports = defineConfig({
  transpileDependencies: [
    'vuetify',
  ],
  productionSourceMap: false,
  publicPath: '/',
  configureWebpack: {
    context: __dirname,
    devServer: {
      host,
      port,
      hot: true,
      https: false,
      headers: { 'Access-Control-Allow-Origin': ['*'] },
      client: {
        logging: 'info',
        webSocketURL: {
          hostname: host,
          port,
        },
      },
      devMiddleware: {
        writeToDisk: true,
      },
    },
    output: {
      path: path.resolve('./dist/'),
      filename: '[name]-[hash].js',
    },
    optimization: {
      splitChunks: false,
    },
    plugins: [
      new BundleTracker({
        path: __dirname,
        filename: './dist/webpack-stats.json',
      }),
      new MiniCssExtractPlugin({
        filename: '[name]-[hash].css',
        chunkFilename: '[name]-[hash].css',
      }),
      new HtmlWebpackPlugin({
        template: './src/index.html',
      }),
    ],
  },
});
