module.exports = function(grunt) {

   // Project configuration.
   grunt.initConfig({
      watch: {
         css: {
          files:  [ 'src/**/*.css' ],
          tasks:  [ 'autoprefixer' ]
         },
         js: {
            files:  [ 'src/**/*.js' ],
            tasks:  [ 'uglify' ]
         }
      },
      autoprefixer: {

          options: {},

          // prefix the specified file
          single_file: {
            options: {},
            src: 'src/style.css',
            dest: 'public/style.css'
          }
      },      
      uglify: {
         my_target: {
            files: {
               'public/app.js': [
                  'src/libraries/**/*.js',
                  'src/app/**/*.js'
               ]
            }
         }
      }
   });

  // Load the plugin that provides the "uglify" task.
  grunt.loadNpmTasks('grunt-contrib-uglify');

  
  grunt.loadNpmTasks('grunt-autoprefixer');

   //  watch
  grunt.loadNpmTasks('grunt-contrib-watch');

  // Default task(s).
  grunt.registerTask('default', ['uglify', 'watch', 'autoprefixer']);

};