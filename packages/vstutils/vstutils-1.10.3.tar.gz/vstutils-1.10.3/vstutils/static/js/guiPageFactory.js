var gui_page_object={getTitle:function()
{if(this.model.data)
{for(let i in this.model.data)
{if(typeof this.model.data[i]=="string")
{return this.model.data[i]}}}
return this.api.name},prefetch:function(data)
{let promise=new $.Deferred();let prefetch_collector=selectPrefetchFieldsFromSchema(this.api.schema.get.fields);if($.isEmptyObject(prefetch_collector.fields))
{return promise.resolve(data);}
var dataFromApi=data.data;selectIdsOfPrefetchFields(dataFromApi,prefetch_collector)
let bulkArr=formBulkRequestForPrefetchFields(prefetch_collector);$.when(this.apiQuery(bulkArr)).done(d=>{addPrefetchInfoToDataFromApi(d,dataFromApi,prefetch_collector);promise.resolve(data);}).fail(f=>{promise.reject(f);})
return promise.promise();},updateFromServer:function()
{let res=this.load(this.model.filters)
$.when(res).done(()=>{for(let i in this.model.guiFields)
{this.model.guiFields[i].updateValue(this.model.data[i],this.model.data)}
this.onUpdateFromServer()})
return res},onUpdateFromServer:function(){},load:function(filters)
{this.model.filters=$.extend(true,{},this.url_vars,filters)
if(typeof this.model.filters!=="object")
{this.model.filters={api_pk:this.model.filters}}
var thisObj=this;var url=this.api.path
if(this.model.filters)
{for(let i in this.model.filters)
{if(/^api_/.test(i))
{url=url.replace("{"+i.replace("api_","")+"}",this.model.filters[i])}}}
let q={data_type:url.replace(/^\/|\/$/g,"").split(/\//g),method:'get'}
var def=this.apiQuery(q);var promise=new $.Deferred();$.when(def).done(data=>{$.when(this.prefetch(data)).always(a=>{thisObj.model.data=a.data
thisObj.model.status=a.status
promise.resolve(a);});}).fail(e=>{promise.reject(e)})
return promise.promise();},init:function(page_options={},url_vars=undefined,object_data=undefined)
{this.base_init.apply(this,arguments)
if(object_data)
{this.model.data=object_data
this.model.status=200
this.model.title+=" #"+this.model.data.id
if(this.api.name_field&&this.model.data[this.api.name_field])
{this.model.title=this.model.data[this.api.name_field]}}},update:function(goUp=false)
{var thisObj=this;var res=this.sendToApi(this.api.methodEdit)
$.when(res).done(function()
{guiPopUp.success("Changes in "+thisObj.api.bulk_name+" were successfully saved");if(goUp)
{vstGO(thisObj.url_vars.baseURL())}})
return res;},delete:function()
{var thisObj=this;if(this.model&&this.model.data&&this.api.parent)
{window.guiListSelections.setSelection(this.api.parent.selectionTag,this.model.data.id)}
var res=this.sendToApi('delete')
$.when(res).done(function()
{guiPopUp.success("Object of '"+thisObj.api.bulk_name+"' type was successfully deleted");})
return res;},renderPage:function(mode,render_options={})
{let tpl=this.getTemplateName('one_'+mode)
if(this.api.autoupdate&&(!render_options||render_options.autoupdate===undefined||render_options.autoupdate))
{this.startUpdates()}
render_options.fields=this.api.schema[mode].fields
render_options.base_path=getUrlBasePath().replace(/\/edit$/,"")
render_options.links=this.api.links
render_options.actions=this.api.actions
this.model.data=this.prepareDataBeforeRender();this.beforeRenderAsPage(mode);tabSignal.emit("guiList.renderPage."+mode+"",{guiObj:this,options:render_options,data:this.model.data,mode:mode});tabSignal.emit("guiList.renderPage."+mode+"."+this.api.bulk_name,{guiObj:this,options:render_options,data:this.model.data,mode:mode});tabSignal.emit("guiList.renderPage",{guiObj:this,options:render_options,data:this.model.data,mode:mode});tabSignal.emit("guiList.renderPage."+this.api.bulk_name,{guiObj:this,options:render_options,data:this.model.data,mode:mode});return spajs.just.render(tpl,{query:"",guiObj:this,opt:render_options,mode:mode});},renderAsEditablePage:function(render_options={})
{return this.renderPage('edit',render_options)},renderAsPage:function(render_options={})
{for(let i in this.api.schema['get'].fields)
{this.api.schema['get'].fields[i].readOnly=true}
return this.renderPage('get',render_options)},beforeRenderAsPage:function(mode)
{this.initAllFields(mode);},prepareDataBeforeRender:function()
{return this.model.data;},}