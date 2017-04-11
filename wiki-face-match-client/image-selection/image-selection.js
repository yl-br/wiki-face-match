angular.module('app').component('imageSelection', {
    templateUrl: 'image-selection/image-selection.html',
    controller: ['$scope','$q','Upload',ImageSelectionController],
    bindings: {
        imageUrls: '=',
        onImageSelectedCallback: '='
    }
});

function ImageSelectionController($scope,$q){
    this.$q = $q;
    this.$scope = $scope;
    this.selected_image = null;
    this.last_uploaded_image = null;
    var self = this;

    $scope.$watch('file', function (newValue) {

        if(newValue) {
            self.file_to_base64(newValue).then(function(file_in_base64){
                self.selected_image = file_in_base64;
                self.last_uploaded_image = file_in_base64;
                self.onImageSelectedCallback(file_in_base64);
            });
        }
    });
}
ImageSelectionController.prototype.on_image_selected = function(image_src, is_url){
    this.selected_image = image_src;
    var self = this;
    if(is_url){
        this.image_url_to_base64(image_src).then(function(file_in_base64){
            self.onImageSelectedCallback(file_in_base64);
        });
    }else{
        self.onImageSelectedCallback(image_src);
    }
};


ImageSelectionController.prototype.file_to_base64 = function (file) {
    var deferred = this.$q.defer();
    var reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = function () {
        deferred.resolve(reader.result);
    };
    reader.onerror = function (error) {
        deferred.reject('Error: ', error);
    };
    return deferred.promise;
}

ImageSelectionController.prototype.image_url_to_base64 = function(url){
    var deferred = this.$q.defer();
    var xhr = new XMLHttpRequest();
    xhr.onload = function() {
        var reader = new FileReader();
        reader.onloadend = function() {
            deferred.resolve(reader.result);
        };
        reader.readAsDataURL(xhr.response);
    };
    xhr.open('GET', url);
    xhr.responseType = 'blob';
    xhr.send();
    return deferred.promise;
}


