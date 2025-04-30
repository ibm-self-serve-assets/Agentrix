module.exports = {
  mode: "development",
  entry: "./src/index.js",
  // entry: path.resolve(__dirname, 'src') + "/app/Hello.jsx",
  // ...,
  // ...,
  resolve: {
    extensions: ['.js', '.jsx', '.ts', '.tsx'],
    root: [path.resolve('./src')],
    fallback: {
      "url": require.resolve("url/")
    }
  },
  
   
    modules: ['.', 'node_modules'],
    plugins: [
      ignore,
    ],
    output: {
      path: path.resolve(__dirname, "dist")
    },
};