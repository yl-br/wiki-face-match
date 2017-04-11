angular.module('app',['ngFileUpload'])
    .constant('wiki_face_match_api_url','http://ec2-54-154-151-3.eu-west-1.compute.amazonaws.com')
    .controller('AppController',['$http','$timeout','Upload','wiki_face_match_api_url',AppController]);

function AppController($http,$timeout,Upload,wiki_face_match_api_url){
    this.Upload = Upload;
    this.$timeout = $timeout;
    this.image_urls = [];
    this.selected_image = null;
    this.display_image = null;
    this.is_loading = false;
    this.match_results = null;
    this.match_error_message = null;
    this.wiki_face_match_api_url = wiki_face_match_api_url
    var self = this;

    $http.get(this.wiki_face_match_api_url + '/randomImages').then(function(res){
        self.image_urls = res.data.map(function(path){
            return 'imdb_crop/' + path;
        });
    })

    this.on_image_selected = function(img_base_64){
        if(self.selected_image != img_base_64){
            self.selected_image = img_base_64;
            self.match_results = null;
            self.match_error_message = null;
        }
        self.display_image =  img_base_64;
    }
}
AppController.prototype.get_image_base64_size = function(image_base64){
    var byteLength = parseInt((image_base64).replace(/=/g,"").length * 0.75);
    var mb_size = parseFloat(byteLength/1024/1024).toPrecision(2);
    return mb_size
}

AppController.prototype.send_image = function(){
    if(!this.selected_image){
        return;
    }
    var self = this;
    this.is_loading = true;
    this.Upload.upload({
        url: self.wiki_face_match_api_url + '/findMatches',
        data: {
            file: self.Upload.dataUrltoBlob(self.selected_image)
        }
    }).then(function (res) {
        self.is_loading = false;
        self.match_results = res.data;
        self.show_boxed_image();
        self.$timeout(function () {
            self.hide_boxed_image();
        },2000);
    },function(error){
        console.log(error);
        self.is_loading = false;
        self.match_error_message = error.data && error.data.message ? error.data.message : 'An error occurred.';
    });
}


AppController.prototype.hide_boxed_image= function(){
    this.display_image = this.selected_image;
}

AppController.prototype.show_boxed_image = function () {
    if(this.match_results && this.match_results['boxed_image']){
        var img = 'data:image/jpeg;base64,' + this.match_results['boxed_image'];
        this.display_image = img;
    }
}
AppController.prototype.is_disable_send_image = function(){
    return !this.selected_image || this.is_loading || this.match_results || this.match_error_message;
}

