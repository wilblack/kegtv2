//console.log = function(){return;}


MenuItem = Backbone.Model.extend({ 
  defaults: {},
});

BeerItem = Backbone.Model.extend({
  
});

OnMenu = Backbone.Collection.extend({
  models:MenuItem,
  url:"/billboard/menuitem/save/",
  save_all: function(){
   this.each(function(menuitem){
      menuitem.save({},{success:function(model, response){
          console.log(response);
        }
      });
   });
  },
  
  
  load_grid: function(){
    /* Loads a Collection of MenuItems into the menu-grid via 
     * the MenuItemView
     * 
     */
    console.log("Entered load_grid")
    this.each(function(item){
      var id = "#"+item.get("position");
      new MenuItemView({el:$(id), model:item});
    });
  }
});

Beers = Backbone.Collection.extend({
  models:BeerItem,
  url:"//",
});

//-------------------- Views -------------------------------

BeerView = Backbone.View.extend({
  /* A view for a single beer
   * 
   */
  
  className: "beer",
  
  render: function(){
    // variable to pass to template
    var variables = make_beer_varaibles(this.model);
    
    // Make attach some stuff to a template
    var template = _.template( $("#beer-item").html(), variables);
    this.el.innerHTML = template;
    return this;
  },
  
});

MenuItemView = Backbone.View.extend({
  // Pass the model in as model.
  initialize: function(){
    this.render();
  },
  
  render: function(){
    // variable to pass to template
    console.log("MenuItemView: Entering render")
    var variables = make_beer_varaibles(this.model);
    console.log(this.model)
    
    // Make attach some stuff to a template
    var template = _.template( $("#beer-item").html(), variables);
    $(this.el).empty()
    console.log(template)
    $(this.el).html(template);
    $(this.el).css("backround-color", this.model.get("color1"));
    this.$(".beer").css("height", "100%");
  },
  
});

BeerCollectionView = Backbone.View.extend({
  /* This is a <ul> list of all beers to choose from
   * Pass in a collection (beerList) and a el (#beer-list)
   * 
   */
  
  initialize: function(){
    var that = this; // so we can use that in underscore mapping function
    this._beerViews = [];
    
    this.collection.each(function(beer){
      that._beerViews.push(new BeerView({
        model:beer,
        tagName:'li', // this is was it will be appended as
      }));
    });
    this.render();
  },
  
  render: function(){
    var that = this;
    $(this.el).empty();
    
    // Render each sub-view and append to the parent view
    _(this._beerViews).each(function(dv){
      $(that.el).append(dv.render().el);
    });
    
    $( ".beer" ).draggable({ //snap: ".grid-cell",
                             revert:"invalid", 
                             opacity: 0.7, 
                             helper: "clone", 
                          });
  },
});


//----------------------------------------------------------

function make_beer_varaibles(model){
  /* Takes in a beer models and returns a dictionary of values used
   * to render a beer menu-item. Used by MenuItemView and BeerView.
   */
  variables = {'cid':model.cid,
               'color1':model.get("color1"),
               'color2':model.get("color2"),
               'color3':model.get("color3"),
               'name':model.get("name"),
               'beer_type':model.get("beer_type"),
               'abv':model.get("abv"),
               'brewery':model.get("brewery"),
               'brewery_city':model.get("brewery_city"),
               'brewery_state':model.get("brewery_state"),
              };
  return variables;
}


/********************** CSRF Stuff. I have no idea what this does *****************/
$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});

