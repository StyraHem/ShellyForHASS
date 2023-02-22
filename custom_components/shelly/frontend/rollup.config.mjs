import livereload from "rollup-plugin-livereload";
import babel from '@rollup/plugin-babel';
import { nodeResolve } from '@rollup/plugin-node-resolve';
import commonjs from '@rollup/plugin-commonjs';
import replace from '@rollup/plugin-replace';
import typescript from "rollup-plugin-typescript2";
import { visualizer } from 'rollup-plugin-visualizer';
import postcss from 'rollup-plugin-postcss'

const production = !process.env.ROLLUP_WATCH;

export default {
  input: "src/index.ts",
  output: {
    file: "../www/bundle.js",
    format: "iife",
    sourcemap: true,
  },
  plugins: [
    typescript(),
    nodeResolve({
      extensions: [".js", ".jsx"] 
    }),
    replace({
     'process.env.NODE_ENV': JSON.stringify( 'development' )
    }),
    babel({
       presets: ["@babel/preset-react"] //, "@babel/preset-flow"],
    }),
    commonjs(),
    postcss({
      inject:  (css, id) => 
      `
          var e = document.createElement("style");
          e.setAttribute("type", "text/css");
          e.appendChild(document.createTextNode(${css}))
          var pnl = document.querySelector("home-assistant").shadowRoot.querySelector("home-assistant-main").shadowRoot;
          pnl.append(e)
        `      
    }),
    visualizer(),
    /*serve({
      open: true,
      verbose: true, 
      contentBase: ["", "public"],
      host: "localhost",
      port: 3000,
    }),*/
    !production && livereload({ watch: "dist" }),
  ]
};
