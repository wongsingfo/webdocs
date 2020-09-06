module.exports = {
    devServer: {
      // Server: 'http://10.128.202.42:8000'
      // LocalServer: 'http://localhost:8000'
      proxy: {
        '^/api/': {
          target: 'http://localhost:8000'
        },
        '^/api-auth/': {
          target: 'http://localhost:8000'
        },
        '^/admin/': {
          target: 'http://localhost:8000'
        },
        '^/static/rest_framework/': {
          target: 'http://localhost:8000'
        }
      }
    },

    // configureWebpack: {
    //   module: {
    //     rules: [
    //       {
    //         test: /\.(png|jpe?g|gif|svg)(\?.*)?$/,
    //         use: {
    //           loader: 'url-loader',
    //           query: {
    //             limit: 10000,
    //             name: 'imgs/[name]--[folder].[ext]'
    //           }
    //         }
    //       },
    //       {
    //         test: /\.(mp4|webm|ogg|mp3|wav|flac|aac)(\?.*)?$/,
    //         loader: 'url-loader',
    //         options: {
    //           limit: 10000,
    //           name: 'media/[name]--[folder].[ext]'
    //         }
    //       },
    //       {
    //         test: /\.(woff2?|eot|ttf|otf)(\?.*)?$/,
    //         use: {
    //           loader: 'url-loader',
    //           query: {
    //             limit: 10000,
    //             name: 'fonts/[name]--[folder].[ext]'
    //           }
    //         }
    //       }
    //     ]
    //   }
    // },

    chainWebpack: config => {
      config
        .plugin('html')
        .tap(options => {
          if (options[0].minify) {
            options[0].minify.minifyCSS = true
          }
          return options
        })

      // config.module
      //   .rule('gzip')
      //   .test(/\.gz$/)
      //   .use('gzip-loader')
      //   .loader('gzip-loader')
      //   .end()

      // config.module
      //   .rule('txt')
      //   .test(/\.txt$/)
      //   .use('@/loaders/txtLoader')
      //   .loader('@/loaders/txtLoader')
      //   .end()
    },

    productionSourceMap: false,
    assetsDir: 'static'
  }
