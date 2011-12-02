//console.log = function(){return;}
ACCENT_COLOR = "white"; 
MAX_ITEMS = 8;
/******************************* MODELS ****************************************/
MenuItem = Backbone.Model.extend({ 
  defaults: {},
});

BeerItem = Backbone.Model.extend({
  
});

Tweet = Backbone.Model.extend({
	  
});

/******************************** END MODELS **********************************/


/******************************* TWEETS ****************************************/
Tweets = Backbone.Collection.extend({
  models:Tweet,
  url:"/broadcast/twitter/get/1/",
  initialize: function(){
  },
  
});

OnMenu = Backbone.Collection.extend({
  /*
   * Models that are actually on the menu as opposed to being able to
   * be on the menu. 
   * This is used in edit only.
   */
	
  models:MenuItem,
  url:"/billboard/menuitem/save/",
  
  // Server save of new menu items.
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
   * Where is this used?
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
	 * 
	 * Uses template #menu-item-detail
	 */
	initialize: function () {
		this.el  = "#menu-detail";
		this.active = 0;
		this.collection = beerList;
		this.model = this.collection.at(this.active);
		this.next();
	  },
	render: function(){
		/*
		 * USed to show an individual menu items detailed info
		 */
	    var variables = make_beer_variables(this.model);
	    	    
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
			//$(".menu-item").css("border","");
			//$(".menu-item").removeClass("menu-item-active");
			this.show_ad();
			this.active = 0;
			beerCollectionView.center_at(0);
		} else {
		
		  var beer = this.collection.at(this.active);
		  this.show_beer(beer);
		  console.log("Active beer cid: "+beer.cid);
		  beerCollectionView.next(this.active);
		  
		  this.active++;
		}
	},
	show_ad: function(){
		html = _.template( $("#ad-template").html());
		$("#menu-detail").html(html);
	}
});

MenuItemView = Backbone.View.extend({
  /* Pass the model in as model.	
   * Used to populate the menu choice in edit page.  
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
   * This is used in show.html to show the list of beers
   * on the brewpub's menu.
   */
  
  initialize: function(draggable){
    var that = this; // so we can use that in underscore mapping function
    this._beerViews = [];
    if(!draggable) this.draggable=false;
      
    // Loop through each beer in the collection
    // And create a BeerView <li> for it.
    
    // Make the list 3 times to account for scrolling
    for (var i=0;i<=2;i++){
	    this.collection.each(function(beer){
	      that._beerViews.push(new BeerView({
	        model:beer,
	        tagName:'li', // this is was it will be appended as
	      }));
	    });
    }   
    
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
  next: function(active_index){
	   //var offset = $("#menu-list").find("li").outerHeight();
	   //offset=offset+6;
	   //
	   this.center_at(active_index);	   
  },
  
  center_at: function(index){
	/*
	 * centers the scrolling menu at the given index.
	 * This means that the menu item with the given index
	 * will be centered on the screen.
	 * 
	 */  
	 obj = this;
	 index=index; // 
	 var offset = $("#menu-list").find("li").outerHeight();
	 
	 offset = ( - obj.collection.length - index + 3) *(offset+3);	
	 console.log("offset: "+offset)
	 $(".menu-item").removeClass("menu-item-active");
	 
	 $(this.el).animate({"top":offset+"px"}, 1*1000, function(){
		 $(obj.el).find("li").eq(index+obj.collection.length)
					.find(".menu-item")
					.addClass("menu-item-active");
	 });
  },
   
});

TwitterFeed = Backbone.View.extend({
	delta_t: 20*1000,
	pos:0,
	initialize: function(){
		tweets.bind("add", this.show_new, this);
		this.render();
		
	},
	render: function(){
		var html='';
		this.collection.each(function(tweet){
			html += tweet.get("text") +" | ";
		});
		$(this.el).html("");
		$(this.el).html(html);
		console.log(html);
	},
	
	update: function(){
		/* Updates the twitter text by checking the server 
		 * for more tweets. This runs indefinitaley
		 */
		var tweets = this.collection;
		var twitterFeed = this;
		window.setTimeout(function(){
			console.log("Fetch new tweets")
			var rs = twitterFeed.fetch();
			twitterFeed.update();
		}, this.delta_t);
	},
	
	show_new: function(that){
		 /*
		  * Function actually show the tweet in the scrolling-feed div.
		  */
		 var text = ""+that.get("user")+ ": "+that.get("text");
		 var html = $("<div>").html(text);
		 
		 $(this.el).append(html);
		 $(this.el).scrollTop($(this.el)[0].scrollHeight);
		 console.log(html);
		 
	 },
			
	fetch: function(){
		/*
		 * Both loads and updates the tweets. IT is called on page load 
		 * and periodically to update tweets. 
		 */
		var url = tweets.url;
		$.get(url, function(data){
			console.log("in ajax callback")
			if (data.length > 0){
				
				data = _.sortBy(data, function(item){
					return item['twitter_id'];
				});
				// If brand new, last_id is set to zero
				// else its set to the new tweet.
				var last_id = 0;
				if (tweets.last()){
					last_id=tweets.last().get("twitter_id");
				}
				
				
				// Sort json array by twiiter id so we can get the last one
				var is_new = _.groupBy(data, function(item){
					if (item["twitter_id"] > last_id){
						return "yes";
					} else {
						return "no";
					}
				});
				console.log(is_new);
				_.each(is_new['yes'], function(item){
					console.log("adding tweet " + item);
					tweets.add(item);
				});
			}
			
		}, 'json');
	},
	
	scroll: function(){
		// This is working properly. If I set overflow:hidden 
		// It doesn't draw all the text so scrolling does not work. 
		this.pos -=2;
		if(this.pos <  -1000){
			this.pos = 0;
		}    
		$(this.el).offset({left:this.pos});
		window.setTimeout(function(){twitterFeed.scroll();},  30);
	},
	
});


//----------------------------------------------------------

function make_beer_variables(model){
  /* Takes in a beer models and returns a dictionary of values used
   * to render a beer menu-item. Used by MenuItemView and BeerView.
   */
  var abv_text = "";
  if (model.get("abv")) abv_text = "ABV: "+model.get("abv")+"%"; 
  
  var ibu_text = "";
  if (model.get("ibu")) ibu_text = "IBU: "+model.get("ibu");
    
  variables = {'cid':model.cid,
               'color1':model.get("color1"),
               'color2':model.get("color2"),
               'color3':model.get("color3"),
               'name':model.get("name"),
               'beer_type':model.get("beer_type"),
               'abv':abv_text,
               'ibu':ibu_text,
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

