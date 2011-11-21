//console.log = function(){return;}
ACCENT_COLOR = "#075F3B"; 

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
  
  load_menu: function(){
      // Loads the menu with the beers on the menu
	  this.each(function(item){
	    //var id = "#"+item.get("position");
	    new MenuItemDetailView({model:item});
	  });	  
  },
    
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
    var variables = make_beer_variables(this.model);
    
    // Make attach some stuff to a template
    var template = _.template( $("#menu-item").html(), variables);
    this.el.innerHTML = template;
    return this;
  },
  
});

MenuItemDetailView = Backbone.View.extend({
	/*
	 * A view to show a single beers template. Pass in the elements as el
	 * and the Beer model as model.
	 */
	initialize: function () {
		this.el  = "#menu-detail";
		this.active = 0;
		this.collection = beerList;
		this.model = this.collection.at(this.active);
		this.next();
	  },
	render: function(){
		// create the variables to pass to menu-item template
	    var variables = make_beer_variables(this.model);
	    
	    // Make attach some stuff to a template
	    var template = _.template( $("#menu-item-detail").html(), variables);
	    $(this.el).empty()
	    $(this.el).html(template);
	},
	show_beer: function(beer){
		/*
		 * Used to update the Menu Item Display. PAss in the 
		 * beer model you want displayed.
		 */
		this.model = beer;
		this.render();
	},
	next: function(that){
		if (this.active == this.collection.length){
			$(".menu-item").css("border","").css("background","#FFF6E8");
			this.show_ad();
			this.active = 0;
		}
		
		var beer = this.collection.at(this.active);
		this.show_beer(beer);
		console.log(beer.cid)
		$(".menu-item").css("border","").css("background","#FFF6E8");
		$("#"+beer.cid).css("border","2px solid "+ACCENT_COLOR)
		               .css("background", "-webkit-linear-gradient(left top, #FFD48E, #FFF6E8, #FFD48E )")
		               .css("background", "-moz-linear-gradient( top left,#FFD48E,#FFF6E8, #FFD48E)");
		this.active++;
	},
	show_ad: function(){
		html = _.template( $("#ad-template").html());
		$("#menu-detail").html(html);
	}
});

MenuItemView = Backbone.View.extend({
  /* Pass the model in as model.	
   * USed to populate the menu choice in edit page.  
   */	
  initialize: function(){
    this.render();
  },
  
  render: function(){
    // create the variables to pass to menu-item template
    var variables = make_beer_variables(this.model);
    
    // Make attach some stuff to a template
    var template = _.template( $("#beer-item").html(), variables);
    $(this.el).empty()
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
  
  initialize: function(draggable){
    var that = this; // so we can use that in underscore mapping function
    this._beerViews = [];
    if(!draggable) this.draggable=false;
        
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
    
    if (this.draggable){
      $( ".beer" ).draggable({ //snap: ".grid-cell",
                               revert:"invalid", 
                               opacity: 0.7, 
                               helper: "clone", 
                             });
    }
  },
      
});


//----------------------------------------------------------

function make_beer_variables(model){
  /* Takes in a beer models and returns a dictionary of values used
   * to render a beer menu-item. Used by MenuItemView and BeerView.
   */
  var abv_text = "";
  if (model.get("abv")) abv_text = "abv: "+model.get("abv")+" %"; 
  
  variables = {'cid':model.cid,
               'color1':model.get("color1"),
               'color2':model.get("color2"),
               'color3':model.get("color3"),
               'name':model.get("name"),
               'beer_type':model.get("beer_type"),
               'abv':abv_text,
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

