var webpack = require('webpack');

module.exports = {
   entry: './app/client.js',
   output: {
       filename: 'bundle.js',
       path: './server/public',
       publicPath: '/'
   },
   module: {
     loaders: [
          {
             test: /\.js$/,
             exclude: /node_modules/,
             loader: 'babel-loader',
             query: {
                     'presets': ['es2015', 'stage-0', 'react'],
                     'plugins': ['transform-decorators-legacy']

             }
          },
          { test: /\.css/, loader: 'style!css' },
          { test: /\.(woff2|woff|ttf|svg|eot)$/, loader: 'file' }
     ]
  },
  externals: {
    'Config': JSON.stringify(require('./version.json'))
  },
  devtool: 'eval-source-map'
};
