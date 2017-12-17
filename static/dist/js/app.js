(function (window, angular) {
	'use strict';
	var wallet = angular.module("wallet", [
		"ui.router"
	]);

	var getTemplate = function (filename) {
		return '/static/views/' + filename;
	}

	let API_ENDPOINT = 'http://127.0.0.1:5000/api/v1/';

	wallet.config([
		'$stateProvider', '$urlRouterProvider', '$httpProvider',
		function ($stateProvider, $urlRouterProvider, $httpProvider) {
			$stateProvider
			.state('auth', {
				url: '/auth',
				abstract: true,
				templateUrl: getTemplate('auth_base.html'),
				controller: 'authBaseController'
			})
			.state('auth.signup', {
				url: '/register',
				templateUrl: getTemplate('auth_signup.html'),
				controller: 'authRegisterController'
			})
			.state('auth.login', {
				url: '/login',
				templateUrl: getTemplate('auth_login.html'),
				controller: 'authLoginController'
			})
			.state('dashboard', {
				url: '/dashboard',
				templateUrl: getTemplate('dashboard.html'),
				resolve : {
					getList : function($rootScope,apiFactory){
						console.log('get list in resolve');
						return apiFactory.getTransactionList($rootScope.userObj.customer.wallet.id,'active');
					}
				},
				controller: 'dashboardController'
			});

			$urlRouterProvider.otherwise(function ($inject) {
				let $state = $inject.get('$state');

				$state.go('auth.login');
			});

			$httpProvider.interceptors.push('myInterceptor');
		}
	]);

	wallet.run([
		'$window', '$rootScope', '$state', 'apiFactory',
		function ($window, $rootScope, $state, apiFactory) {
			$rootScope.userObj = $window.localStorage.userObj ? JSON.parse($window.localStorage.userObj) : null;
			$rootScope.$on("$stateChangeStart", function (event, toState, fromState, toParams, fromParams) {

				console.log(event, toState, fromState, toParams, fromParams);
				if(!$rootScope.userObj && toState.name == 'dashboard') {
					console.log('condition true',$rootScope.userObj,toState.name);
					$state.go('auth.login');
					return;
				}
			});
		}
	]);

	wallet.factory('myInterceptor', [
		'$q', '$window',
		function ($q, $window) {
			return {
				request: function (config) {
					console.log('congig',config);
					if(config && config.headers && $window.localStorage.userObj) {
						config.headers['access-token'] = JSON.parse($window.localStorage.userObj)['access-token'];
					}

					return config;
				},
				requestError: function (rejection) {
					return $q.reject(rejection);
				},
				response: function (response) {
					return response;
				},
				responseError: function (rejection) {
					return $q.reject(rejection);
				}
			}
		}
	]);

	wallet.factory('apiFactory', [
		'$http', '$q',
		function ($http, $q) {
			let ajax = function (URL, METHOD, DATA) {
				let deferred = $q.defer();

				$http({
					url: URL,
					method: METHOD,
					data: DATA
				})
				.then(function (response) {
					deferred.resolve(response);
				}, function (rejection) {
					deferred.reject(rejection);
				});

				return deferred.promise;
			}

			return {
				legacyLogin: function (entity) {
					let URL = API_ENDPOINT + 'login/legacy',
						METHOD = 'POST',
						DATA = entity;
					return ajax(URL, METHOD, DATA);
				},
				logout: function () {
					let URL = API_ENDPOINT + 'logout',
						METHOD = 'GET';
					return ajax(URL, METHOD);
				},
				signup: function (entity) {
					let URL = API_ENDPOINT + 'register',
						METHOD = 'POST',
						DATA = entity;
					return ajax(URL, METHOD, DATA);
				},
				getTransactionList : function (wallet_id,type){
					let URL = API_ENDPOINT + 'wallet/'+wallet_id+'/transactions?type='+type,
						METHOD = 'GET';
					return ajax(URL, METHOD);
				},
				cancelTransaction:function(wallet_id,transactions_id){
					let URL = API_ENDPOINT + 'wallet/'+ wallet_id +'/transactions/'+transactions_id,
					METHOD = 'DELETE';
					return ajax(URL,METHOD);
				},
				newTransaction:function(wallet_id,data){
					let URL = API_ENDPOINT +'wallet/'+wallet_id + '/transactions',
					METHOD = 'POST',
					DATA = data;
					return ajax(URL,METHOD,DATA);
				},
				pagination:function(url){
					let URL = url, METHOD='GET';
					return ajax(URL, METHOD);
				}
			}
		}
	]);

	wallet.controller('authBaseController', [
		'$scope',
		function ($scope) {
			$scope.helo = "Auth base"
		}
	]);

	wallet.controller('authRegisterController', [
		'$window', '$rootScope', '$scope', '$state', 'apiFactory',
		function ($window, $rootScope, $scope, $state, apiFactory) {
			$scope.user = {
				email: '',
				password: '',
				rePassword: '',
				displayName: ''
			}
			$scope.errorMsg = '';
			$scope.signup = function () {
				apiFactory.signup($scope.user).then(
					function (response) {
						$rootScope.userObj = response.data.data;
						$window.localStorage.userObj = JSON.stringify(response.data.data);
						$state.go('dashboard');
					},
					function (rejection) {
						$scope.errorMsg = rejection.data.notification.message;
					}
				)
			}
		}
	]);

	wallet.controller('authLoginController', [
		'$window', '$rootScope', '$scope', '$state', 'apiFactory',
		function ($window, $rootScope, $scope, $state, apiFactory) {
			$scope.user = {
				email: '',
				password: ''
			}
			$scope.errorMsg = '';

			$scope.legacyLogin = function () {
				apiFactory.legacyLogin($scope.user).then(
					function (response) {
						$rootScope.userObj = response.data.data;
						$window.localStorage.userObj = JSON.stringify(response.data.data);
						$state.go('dashboard');
					},
					function (rejection) {
						$scope.errorMsg = rejection.data.notification.message;
					}
				);
			}
			// $scope.googleLogin = function () {
			// 	apiFactory.googleLogin($scope.user).then(
			// 		function (response) {
			// 			$rootScope.userObj = response.data.data;
			// 			$window.localStorage.userObj = JSON.stringify(response.data.data);
			// 			$state.go('dashboard');
			// 		},
			// 		function (rejection) {

			// 		}
			// 	);
			// }

		}
	]);

	wallet.controller('dashboardController', [
		'$scope','$rootScope','apiFactory','getList','$window', '$state',
		function ($scope,$rootScope,apiFactory,getList,$window,$state) {
			console.log('dashboardController',getList);
			$scope.userDetails = $rootScope.userObj;
			$scope.wallet = $rootScope.userObj.customer.wallet;
			$scope.transactionList = getList.data;
			$scope.status = 'active';

			$scope.getList = function(type){
				apiFactory.getTransactionList($scope.wallet.id,type).then(function(response){
					$scope.transactionList = response.data;
				})
			}
			$scope.pagination = function(url){
				apiFactory.pagination(url).then(function(response){
					$scope.transactionList = response.data;
				})
			}

			$scope.changeStatus = function(type){
				$scope.status = type;
				$scope.getList($scope.status);
			}

			$scope.updateWallet = function(response){
				$rootScope.userObj.customer.wallet.currentBalance = response.data.data.wallet.currentBalance;
				$rootScope.userObj.customer.wallet.lastTransactionDate = response.data.data.wallet.lastTransactionDate;
				$scope.wallet = $rootScope.userObj.customer.wallet;
				$window.localStorage.userObj = JSON.stringify($rootScope.userObj);

			}

			$scope.openModal = function(){
				$scope.transaction = {};
				$('#transactionModal').modal('show');
			}

			$scope.createTransaction = function(){
				apiFactory.newTransaction($scope.wallet.id,$scope.transaction).then(function(response){
					$('#transactionModal').modal('hide');
					$scope.getList('active');
					$scope.updateWallet(response);
				})
			}

			$scope.cancelTransaction = function(data,index){
				if(data.transactionType == 'CREDIT' && data.transactionAmount > $scope.wallet.currentBalance){
					window.alert("Insufficient balance for cancellation");
				}
				else{
					apiFactory.cancelTransaction($scope.wallet.id,data.id).then(function(response){
						$scope.transactionList.data.splice(index,1);
						$scope.transactionList.data.unshift(response.data.data);
						$scope.updateWallet(response);
					})
				}
			}

			$scope.userLogout = function () {
				apiFactory.logout().then(
					function (response) {
						$rootScope.userObj = null;
						delete $window.localStorage.userObj;
						$state.go('auth.login');
					},
					function (rejection) {
						$scope.errorMsg = rejection.data.notification.message;
					})
				}

		}
	]);
}(window, angular))