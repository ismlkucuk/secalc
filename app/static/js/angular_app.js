var app = angular.module("section", []);

// angular config
app.config(['$interpolateProvider', function($interpolateProvider) {
  $interpolateProvider.startSymbol('{-');
  $interpolateProvider.endSymbol('-}');
}]);



// defineSection Controller
app.controller("defineSection", function($scope, $rootScope, $http) {
    $scope.types = [];
    $scope.selectedType = null;
    $scope.sections = [];
    $scope.selectedSection = null;

    $scope.refreshSectionTypes = function() {
        $http.get("http://localhost:8888/structures/section_types")
        .then(function(response) {
            $scope.types = response.data;
            $scope.selectedType = null;
        });
    };


    $scope.custom_section = {
        name: '',
        type_id: 0,
        parameters: {}
    };

    $scope.selectedTypeChanged = function() {
        $scope.custom_section.parameters = {};
        for (i = 0; i < $scope.selectedType.parameters.length; i++){
            $scope.custom_section.parameters[$scope.selectedType.parameters[i]] = 0.0;
        }

        $scope.selectedSection = $scope.custom_section;

        $http.get($scope.selectedType._links.sections.external)
        .then(function(response) {
            $scope.sections = response.data;
            //$scope.selectedSection = null;
        });
    }

    $scope.selectedSectionChanged = function() {
        if ($scope.selectedSection == null) {
            $scope.selectedSection = $scope.custom_section;
        }
        else {
            $http.get($scope.selectedSection._links.details.external)
            .then(function(response) {
                $scope.selectedSection = response.data;
            });
        }
    }

    $scope.add = function() {
        $rootScope.$emit('refresh');

        if ($scope.selectedType == null){
            alert("You must select a section type!");
            return;
        }
        if ($scope.selectedSection.name == ""){
            alert("Name field cannot be empty!");
            return;
        }

        $scope.selectedSection.type_id = $scope.selectedType.id;

        $http({ method: "POST", url: 'http://localhost:8888/structures/custom_section', data: $scope.selectedSection, cache: false })
        .success(function(response) {
            alert(JSON.stringify(response));
        })
        .error(function(response) {
            alert(response.message);
        });


    }


    // Initialize
    $scope.refreshSectionTypes();

});


// listSection Controller
app.controller("listSections", function($scope, $rootScope, $http) {
    $scope.selectedSection = null;

    $scope.refreshSectionList = function(){
        $http.get("http://localhost:8888/structures/sections")
        .then(function(response) {
            $scope.sections = response.data;
            $scope.selectedSection = null;
        });
    };

    $scope.updateSectionProperties = function() {
        $http.get($scope.selectedSection._links.details.external)
        .then(function(response) {
            $scope.sectionDetails = response.data;
        });
    }

    $rootScope.$on('refresh', function() {
        $scope.refreshSectionList();
    });

    $scope.refreshSectionList();
});
