var Typer={text:null,accessCountimer:null,index:0,speed:0.5,file:"",accessCount:0,deniedCount:0,init:function(){$.get(Typer.file,function(data){Typer.text=data;Typer.text=Typer.text.slice(0,Typer.text.length-1);});},content:function(){return $("#console").html();},write:function(str){$("#console").append(str);return false;},makeAccess:function(){Typer.hidepop();Typer.accessCount=0;var ddiv=$("<div id='gran'>").html("");ddiv.addClass("accessGranted");ddiv.html("<h1>ACCESS GRANTED</h1>");$(document.body).prepend(ddiv);return false;},makeDenied:function(){Typer.hidepop();Typer.deniedCount=0;var ddiv=$("<div id='deni'>").html("");ddiv.addClass("accessDenied");ddiv.html("<h1>ACCESS DENIED</h1>");$(document.body).prepend(ddiv);return false;},hidepop:function(){$("#deni").remove();$("#gran").remove();},addText:function(key){if(key.keyCode==18){Typer.accessCount++;if(Typer.accessCount>=3){Typer.makeAccess();}}else if(key.keyCode==20){Typer.deniedCount++;if(Typer.deniedCount>=3){Typer.makeDenied();}}else if(key.keyCode==27){Typer.hidepop();}else if(Typer.text){var cont=Typer.content();if(cont.substring(cont.length-1,cont.length)=="|")$("#console").html($("#console").html().substring(0,cont.length-1));if(key.keyCode!=8){Typer.index+=Typer.speed;}else{if(Typer.index>0)Typer.index-=Typer.speed;}var text=Typer.text.substring(0,Typer.index)
var rtn=new RegExp("\n","g");$("#console").html(text.replace(rtn,"<br/>"));}if(key.preventDefault&&key.keyCode!=122){key.preventDefault()};if(key.keyCode!=122){key.returnValue=false;}},updLstChr:function(){var cont=this.content();if(cont.substring(cont.length-1,cont.length)=="|")$("#console").html($("#console").html().substring(0,cont.length-1));else
this.write("|");}}
function replaceUrls(text){var http=text.indexOf("http://");var space=text.indexOf(".me ",http);if(space!=-1){var url=text.slice(http,space-1);return text.replace(url,"<a href=\""+url+"\">"+url+"</a>");}else{return text}}var timer=null;function t(){Typer.addText({"keyCode":123748});if(Typer.index>Typer.text.length){clearInterval(timer);}}$(window).bind('scroll',function(){var aboutPosition=$("#about").position().top;var y_scroll_pos=window.pageYOffset;if((y_scroll_pos+500)>=aboutPosition){timer=setInterval("t();",30);Typer.speed=0.5;Typer.file=$("#hidden-resume").val();Typer.init();}});
