guiLocalSettings.setIfNotExists('hide_non_required',4)
guiLocalSettings.setIfNotExists('page_size',20)
function getMenuIdFromApiPath(path){return path.replace(/[^A-z0-9\-]/img,"_")}
function guiTestUrl(regexp,url)
{url=url.replace(/[/#]*$/,"").replace(/^\//,"")
let reg_exp=XRegExp(regexp,'x');if(!XRegExp.test(url,reg_exp))
{return false;}
return XRegExp.exec(url,reg_exp)}
all_regexp=[]
function guiGetTestUrlFunctionfunction(regexp,api_path_value)
{all_regexp.push({path:api_path_value.path,regexp:regexp})
return function(url)
{var res=guiTestUrl(regexp,url)
if(!res)
{return false;}
let obj={}
for(let i in res)
{if(/^[0-9]+$/.test(i))
{continue;}
if(i.indexOf("api_")==0&&res[i][0]=='@')
{obj[i]=res[i].substring(1)}
else
{obj[i]=res[i]}}
obj.url=res[0]
obj.page_and_parents=res[0]
if(obj.page)
{let xregexpItem=XRegExp(`(?<parent_type>[A-z]+)\/(?<parent_id>[0-9]+)\/(?<page_type>[A-z\/]+)$`,'x');let match=XRegExp.exec(obj.page,xregexpItem)
if(match)
{obj.parent_type=match.parent_type
obj.parent_id=match.parent_id
obj.page_type=match.page_type.replace(/\/[A-z]+$/,"")
obj.page_name=match.page_type}}
obj.searchURL=function(query){let url=this.page_and_parents
url=url.replace(this.search_part,"")
url+="/search/"+query
if(this.page_part)
{url=url.replace(this.page_part,"")}
return vstMakeLocalUrl(url);}
obj.baseURL=function(){let arr=[this.page_and_parents.replace(/\/[^/]+$/,"")]
for(let i=0;i<arguments.length;i++)
{arr.push(arguments[i])}
return vstMakeLocalUrl(arr)}
obj.getApiPath=function(){return{api:api_path_value,url:this}}
return obj}}
function getNameForUrlRegExp(api_path)
{return api_path.replace(/\{([A-z]+)\}\//g,"(?<api_$1>[0-9,]+|@[A-z0-9_\-]+)\/").replace(/\/$/,"").replace(/^\//,"").replace(/\//g,"\\/")}
function openApi_add_one_action_page_path(api_obj)
{let api_path=api_obj.path
let page_url_regexp="^(?<parents>[A-z]+\\/[0-9]+\\/)*(?<page>"+getNameForUrlRegExp(api_path.toLowerCase().replace(/\/([A-z0-9]+)\/$/,"/"))+")\\/(?<action>"+api_obj.name+")$"
let regexp_in_other=guiGetTestUrlFunctionfunction(page_url_regexp,api_obj);spajs.addMenu({id:getMenuIdFromApiPath(api_path),url_parser:[regexp_in_other],priority:api_obj.level,debug:api_obj.path,onOpen:function(holder,menuInfo,data,onClose_promise)
{let pageItem=new guiObjectFactory(api_obj)
window.curentPageObject=pageItem
var def=new $.Deferred();def.resolve(pageItem.renderAsPage())
$.when(onClose_promise).always(()=>{pageItem.stopUpdates();})
return def.promise();},})}
function openApi_add_one_page_path(api_obj)
{let api_path=api_obj.path
let page_url_regexp="^(?<parents>[A-z]+\\/[0-9]+\\/)*(?<page>"+getNameForUrlRegExp(api_path)+")$"
let regexp_in_other=guiGetTestUrlFunctionfunction(page_url_regexp,api_obj);spajs.addMenu({id:getMenuIdFromApiPath(api_path),url_parser:[regexp_in_other],priority:api_obj.level,onOpen:function(holder,menuInfo,data,onClose_promise)
{let pageItem=new guiObjectFactory(api_obj)
window.curentPageObject=pageItem
var def=new $.Deferred();$.when(pageItem.load(data.reg)).done(function()
{if(pageItem.api.canEditInView)
{def.resolve(pageItem.renderAsEditablePage())}
else
{def.resolve(pageItem.renderAsPage())}}).fail(function(err)
{def.resolve(renderErrorAsPage(err));})
$.when(onClose_promise).always(()=>{pageItem.stopUpdates();})
return def.promise();},})
if(api_obj.canEdit)
{let page_edit_url_regexp="^(?<parents>[A-z]+\\/[0-9]+\\/)*(?<page>"+getNameForUrlRegExp(api_path)+")/edit$"
let regexp_edit_in_other=guiGetTestUrlFunctionfunction(page_edit_url_regexp,api_obj);spajs.addMenu({id:getMenuIdFromApiPath(api_path+"edit"),url_parser:[regexp_edit_in_other],priority:api_obj.level,onOpen:function(holder,menuInfo,data,onClose_promise)
{let pageItem=new guiObjectFactory(api_obj)
window.curentPageObject=pageItem
var def=new $.Deferred();$.when(pageItem.load(data.reg)).done(function()
{def.resolve(pageItem.renderAsEditablePage())}).fail(function(err)
{def.resolve(renderErrorAsPage(err));})
$.when(onClose_promise).always(()=>{pageItem.stopUpdates();})
return def.promise();},})}}
function openApi_add_list_page_path(api_obj)
{let path_regexp=[]
let api_path=api_obj.path
let pathregexp="^"
+"(?<page_and_parents>"
+"(?<parents>[A-z]+\\/[0-9]+\\/)*"
+"(?<page>"+getNameForUrlRegExp(api_path)+"))"
+"(?<search_part>\\/search\\/(?<search_query>[A-z0-9 %\-.:,=]+)){0,1}"
+"(?<page_part>\\/page\\/(?<page_number>[0-9]+)){0,1}$"
path_regexp.push(guiGetTestUrlFunctionfunction(pathregexp,api_obj))
if(api_obj.canCreate)
{let new_page_url=guiGetTestUrlFunctionfunction("^(?<parents>[A-z]+\\/[0-9]+\\/)*(?<page>"+getNameForUrlRegExp(api_path)+")\\/new$",api_obj)
spajs.addMenu({id:getMenuIdFromApiPath(api_path+"_new"),url_parser:[new_page_url],priority:api_obj.level,onOpen:function(holder,menuInfo,data)
{let pageItem=new guiObjectFactory(api_obj)
window.curentPageObject=pageItem
return pageItem.renderAsNewPage()},})}
if(api_obj.canAdd)
{var add_page_url=guiGetTestUrlFunctionfunction("^(?<page_and_parents>(?<parents>[A-z]+\\/[0-9]+\\/)*(?<page>"+getNameForUrlRegExp(api_path)+"\\/add))(?<search_part>\\/search\\/(?<search_query>[A-z0-9 %\-.:,=]+)){0,1}(?<page_part>\\/page\\/(?<page_number>[0-9]+)){0,1}$",api_obj)
spajs.addMenu({id:getMenuIdFromApiPath(api_path+"_add"),url_parser:[add_page_url],priority:api_obj.level,onOpen:function(holder,menuInfo,data,onClose_promise)
{let pageItem=new guiObjectFactory(api_obj.shortestURL)
window.curentPageObject=pageItem
let filter=$.extend(true,data.reg)
filter.parent_id=undefined
filter.parent_type=undefined
var def=new $.Deferred();$.when(pageItem.search(filter)).done(function()
{def.resolve(pageItem.renderAsAddSubItemsPage())}).fail(function(err)
{def.resolve(renderErrorAsPage(err));})
$.when(onClose_promise).always(()=>{pageItem.stopUpdates();})
return def.promise();},})}
spajs.addMenu({id:getMenuIdFromApiPath(api_path),url_parser:path_regexp,priority:api_obj.level,onOpen:function(holder,menuInfo,data,onClose_promise)
{let pageItem=new guiObjectFactory(api_obj)
window.curentPageObject=pageItem
var def=new $.Deferred();$.when(pageItem.search(data.reg)).done(function()
{def.resolve(pageItem.renderAsPage())}).fail(function(err)
{def.resolve(renderErrorAsPage(err));})
$.when(onClose_promise).always(()=>{pageItem.stopUpdates();})
return def.promise();},onClose:function(){}})}
tabSignal.connect("resource.loaded",function()
{$.when(window.api.init()).done(function()
{tabSignal.emit("openapi.loaded",{api:window.api});$.when(getGuiSchema()).done(function()
{window.guiSchema.path=returnParentLinks(window.guiSchema.path);emitFinalSignals()}).fail(()=>{window.guiSchema=openApi_guiSchema(window.api.openapi);tabSignal.emit("openapi.schema",{api:window.api,schema:window.guiSchema});let guiSchemaForCache={path:deleteParentLinks(window.guiSchema.path),object:window.guiSchema.object,}
guiFilesCache.setFile('guiSchema',JSON.stringify(guiSchemaForCache));window.guiSchema.path=returnParentLinks(window.guiSchema.path);emitFinalSignals();})})})
function getGuiSchema()
{let def=new $.Deferred();if(notUseCache()=="true")
{def.reject();}
else
{$.when(getGuiSchemaFromCache()).done(data=>{def.resolve();}).fail(f=>{def.reject();})}
return def.promise();}
function getGuiSchemaFromCache()
{let def=new $.Deferred();let guiSchemaFromCache=guiFilesCache.getFile('guiSchema');guiSchemaFromCache.then(result=>{window.guiSchema=JSON.parse(result.data);def.resolve();},error=>{def.reject();})
return def.promise();}
function deleteParentLinks(path_obj)
{let del_func=deleteByPatternInSchema(path_obj,'__func__')
let del_link=deleteByPatternInSchema(path_obj,'__link__')
let action=[]
for(let i in del_func)
{action.push("delete path_obj"+del_func[i])}
for(let i in del_link)
{action.push("delete path_obj"+del_link[i])}
eval(action.join(";"))
return path_obj;}
function deleteByPatternInSchema(obj,pattern,max_level=0,level=0,path="",objects=[])
{if(!obj)
{return undefined;}
if(level>20)
{console.warn(obj,pattern,max_level,level)
debugger;throw"Error level > "+level}
if(max_level&&max_level<=level)
{debugger;return undefined;}
if(typeof obj!='object')
{return undefined;}
for(var i in obj)
{if(i.indexOf(pattern)==0)
{objects.push(path+"['"+i.replace(pattern,"")+"']")
continue;}
if(typeof obj[i]=='object')
{if(obj["__link__"+i])
{}
else
{deleteByPatternInSchema(obj[i],pattern,max_level,level+1,""+path+"['"+i+"']",objects)}}}
return objects;}
function returnParentLinks(path_obj)
{let del_func=getFunctionNameBySchema(path_obj,'__func__',(obj,key)=>{if(!window[obj[key]])
{throw"error function "+obj[key]+" not exists"}
return window[obj[key]];})
let del_links=getFunctionNameBySchema(path_obj,'__link__',(obj,key)=>{if(!path_obj[obj[key]])
{throw"error link "+obj[key]+" not exists"}
return path_obj[obj[key]];})
let action=[]
for(let i in del_func)
{action.push("delete path_obj"+del_func[i])}
for(let i in del_links)
{action.push("delete path_obj"+del_links[i])}
eval(action.join(";"))
return path_obj;}
function emitFinalSignals()
{emitSchemaPathSignals(window.guiSchema.path);openApi_guiPagesBySchema(window.guiSchema)
tabSignal.emit("openapi.paths",{api:window.api});tabSignal.emit("openapi.completed",{api:window.api});tabSignal.emit("loading.completed");}