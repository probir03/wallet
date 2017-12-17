let gulp = require('gulp'),
	rename = require('gulp-rename'),
	concat = require('gulp-concat');

let paths = {
	"node": "./node_modules/",
	"dist": "./static/dist/",
	"static": "./static/"
}

let appTask = function () {
	return gulp.src([
		paths.static + 'js/*.js'
	])
	.pipe(concat('app.js'))
	.pipe(gulp.dest(paths.dist + 'js'));
}

let vendorTask = function () {
	return gulp.src([
		paths.node + 'jquery/dist/jquery.min.js',
		paths.node + 'popper.js/dist/umd/popper.min.js',
		paths.node + 'bootstrap/dist/js/bootstrap.min.js',
		paths.node + 'angular/angular.min.js',
		paths.node + 'angular-ui-router/release/angular-ui-router.min.js',

	])
	.pipe(concat('vendor.js'))
	.pipe(gulp.dest(paths.dist + 'js'));
}

let styleTask = function () {
	return gulp.src([
		paths.node + 'bootstrap/dist/css/bootstrap.min.css'
	])
	.pipe(concat('vendor.css'))
	.pipe(gulp.dest(paths.dist + 'css'));
}

let cssTask = function () {
	return gulp.src([
		paths.static + 'css/*.css'
	])
	.pipe(concat('app.css'))
	.pipe(gulp.dest(paths.dist + 'css'));
}

gulp.task('app', appTask);
gulp.task('vendor', vendorTask);
gulp.task('style', styleTask);
gulp.task('css', cssTask);

gulp.task('default', ['style', 'css', 'vendor', 'app']);
