guiLocalSettings.setIfNotExists('page_update_interval',15000)
var gui_base_object={getTemplateName:function(type,default_name)
{var tpl=this.api.bulk_name+'_'+type
if(!spajs.just.isTplExists(tpl))
{if(default_name)
{return default_name;}
return'entity_'+type}
return tpl;},getTitle:function()
{return this.api.name},stopUpdates:function()
{this.update_stoped=true
clearTimeout(this.update_timoutid)},startUpdates:function()
{if(this.update_timoutid)
{return;}
if(this.update_stoped===true)
{return;}
this.update_timoutid=setTimeout(()=>{this.update_timoutid=undefined
if(!this.model.filters||Visibility.state()=='hidden')
{console.warn("startUpdates [no filters]")
this.startUpdates()
return;}
$.when(this.updateFromServer()).always(()=>{console.log("startUpdates [updated]")
this.startUpdates()})},guiLocalSettings.get('page_update_interval'))},updateFromServer:function()
{return false;},initAllFields:function(schema_name)
{for(let i in this.api.schema[schema_name].fields)
{this.initField(this.api.schema[schema_name].fields[i]);}},initField:function(field)
{if(!this.model.guiFields[field.name])
{if(!this.model.guiFields[field.name])
{let type=getFieldType(field,this.model)
var field_value=undefined
if(this.model.data){field_value=this.model.data[field.name]}
this.model.guiFields[field.name]=new window.guiElements[type](field,field_value,this)}}},renderAllFields:function(opt)
{let html=[]
for(let i in opt.fields)
{if(this.api.hide_non_required&&this.api.hide_non_required<Object.keys(opt.fields).length){opt.fields[i].hidden_button=true;}
html.push(this.renderField(opt.fields[i],opt));}
let id=getNewId();return JUST.onInsert('<div class="fields-block" id="'+id+'" >'+html.join("")+'</div>',()=>{let fields=$('#'+id+" .gui-not-required")
if(!this.api.hide_non_required||this.api.hide_non_required>=fields.length)
{return;}
fields.addClass("hidden-field")
$('#'+id).appendTpl(spajs.just.render('show_not_required_fields',{fields:fields,opt:opt}))})},renderField:function(field,render_options)
{let parent_field_name=undefined
if(field.additionalProperties&&field.additionalProperties.field)
{parent_field_name=field.additionalProperties.field}
if(field.parent_field)
{parent_field_name=field.parent_field}
if(!Array.isArray(parent_field_name))
{parent_field_name=[parent_field_name]}
let thisField=this.model.guiFields[field.name];for(let i in parent_field_name)
{let parentField=this.model.guiFields[parent_field_name[i]];if(parentField&&parentField.addOnChangeCallBack)
{parentField.addOnChangeCallBack(function(){thisField.updateOptions.apply(thisField,arguments);})}}
return this.model.guiFields[field.name].render($.extend({},render_options))},getValue:function(hideReadOnly)
{var obj={}
let count=0;for(let i in this.model.guiFields)
{if(this.model.guiFields[i].opt.readOnly&&hideReadOnly)
{continue;}
let val=this.model.guiFields[i].getValidValue(hideReadOnly);if(val!==undefined&&val!==null&&!(typeof val=="number"&&isNaN(val)))
{obj[i]=val;}
count++;}
if(count==1&&this.model.guiFields[0])
{obj=obj[0]}
return obj;},pkValuePriority:["id","pk","name"],getPkValue:function(obj)
{let id;for(let i in this.pkValuePriority){let field=this.pkValuePriority[i];if(obj[field]!==undefined){id=obj[field];break;}}
return id;},getPkValueForUrl:function(obj)
{let id=this.getPkValue(obj);if(id!==undefined&&isNaN(Number(id))){id="@"+id;}
return id;},base_init:function(api_object,url_vars={},object_data=undefined)
{this.url_vars=$.extend(true,{},spajs.urlInfo.data.reg,url_vars)
this.model.title=this.api.bulk_name},init:function()
{this.base_init.apply(this,arguments)},apiQuery:function()
{return api.query.apply(api,arguments)},getDataFromForm:function(method)
{let data=this.getValue(true)
if(this['onBefore'+method])
{data=this['onBefore'+method].apply(this,[data]);}
return data},sendToApi:function(method,callback,error_callback,data)
{var def=new $.Deferred();try{if(!data)
{data=this.getDataFromForm(method)}
if(data==undefined||data==false)
{def.reject()
if(error_callback)
{if(error_callback(data)===false)
{return;}}
return def.promise();}
if(data==true)
{if(callback)
{if(callback(data)===false)
{return;}}
def.resolve()
return def.promise();}
if(!this.api.schema[this.api.method[method]]||!this.api.schema[this.api.method[method]].operationId)
{debugger;throw"!this.schema[this.api.method[method]].operationId"}
let operationId=this.api.schema[this.api.method[method]].operationId.replace(/(set)_([A-z0-9]+)/g,"$1-$2")
var operations=[]
operations=operationId.split("_");for(let i in operations)
{operations[i]=operations[i].replace("-","_")}
var query=[]
var url=this.api.path
if(this.url_vars)
{for(let i in this.url_vars)
{if(/^api_/.test(i))
{url=url.replace("{"+i.replace("api_","")+"}",this.url_vars[i])}}
for(let i in this.url_vars)
{if(/^api_/.test(i))
{if(typeof this.url_vars[i]!="string")
{this.url_vars[i]=this.url_vars[i]+""}
if(this.url_vars[i].indexOf(",")!=-1)
{let ids=this.url_vars[i].split(",")
for(let j in ids)
{query.push(url.replace(this.url_vars[i],ids[j]))}
continue;}}}}
if(query.length==0)
{query=[url]}
query.forEach(qurl=>{qurl=qurl.replace(/^\/|\/$/g,"").split(/\//g)
let q={data_type:qurl,data:data,method:method}
$.when(this.apiQuery(q)).done(data=>{if(callback)
{if(callback(data)===false)
{return;}}
if(data.not_found>0)
{guiPopUp.error("Item not found");def.reject({text:"Item not found",status:404})
return;}
def.resolve(data)}).fail(e=>{if(callback)
{if(error_callback(e)===false)
{return;}}
this.showErrors(e,q.method)
def.reject(e)})})}catch(e){webGui.showErrors(e)
def.reject()
if(e.error!='validation')
{throw e}}
return def.promise();},showErrors:function(error,method){tabSignal.emit('guiItemFactory.showErrors',{thisObj:this,api_response:error,query_method:method})
if(!error)
{return}
debugger;if(!error.status||error.status<400)
{return webGui.showErrors(error)}
let text=""
if(error.data.detail)
{text=error.data.detail+". "}
if(this.api.schema[this.api.method[method]]&&this.api.schema[this.api.method[method]].responses&&this.api.schema[this.api.method[method]].responses[error.status]&&this.api.schema[this.api.method[method]].responses[error.status].description)
{text+=this.api.schema[this.api.method[method]].responses[error.status].description}
else if(this.api.schema[method]&&this.api.schema[method].responses&&this.api.schema[method].responses[error.status]&&this.api.schema[method].responses[error.status].description)
{text+=this.api.schema[method].responses[error.status].description}
return guiPopUp.error(text)}}
function guiObjectFactory(api_object)
{if(!api_object)
{console.error('Path api_object is '+typeof api_object)
debugger;}
if(typeof api_object=="string")
{if(!window.guiSchema.path[api_object])
{console.error('Path \`{path}\` doesn\'t exist'.format({path:api_object+""}))
debugger;}
api_object=window.guiSchema.path[api_object]}
this.model={selectedItems:{},guiFields:{}}
let arr=[this,window.gui_base_object]
if(window["gui_"+api_object.type+"_object"])
{arr.push(window["gui_"+api_object.type+"_object"])}
if(api_object.extension_class_name)
{for(let i in api_object.extension_class_name)
{if(api_object.extension_class_name[i]&&window[api_object.extension_class_name[i]])
{arr.push(window[api_object.extension_class_name[i]])}}}
arr.push({api:api_object})
$.extend.apply($,arr)
this.init.apply(this,arguments)}
function emptyAction(action_info,guiObj,dataLine=undefined)
{let url_vars=$.extend(true,{},guiObj.url_vars)
if(dataLine)
{let keys=action_info.path.match(/{([^\}]+)}/g)
for(let i in keys)
{let key=keys[i].slice(1,keys[i].length-1)
if(url_vars['api_'+key]===undefined)
{url_vars['api_'+key]=dataLine.url_key}}}
var pageItem=new guiObjectFactory(action_info,url_vars)
return function(){return pageItem.exec()}}
function deleteAndGoUp(obj)
{var def=obj.delete();$.when(def).done(function(){var upper_url=spajs.urlInfo.data.reg.baseURL().replace(/\/\d+$/g,'');vstGO(upper_url);})
return def;}
function goToMultiAction(ids,action,selection_tag)
{if(action&&action.isEmptyAction)
{let pageItem;let url_info=spajs.urlInfo.data.reg;if(!url_info.parent_type){url_info["api_pk"]=ids.join(",");}else{url_info["api_"+url_info.page_name+"_id"]=ids.join(",");}
pageItem=new guiObjectFactory(action,url_info);pageItem.exec();window.guiListSelections.unSelectAll(selection_tag);return false;}
return vstGO([spajs.urlInfo.data.reg.page_and_parents,ids.join(","),action.name]);}
function goToMultiActionFromElements(elements,action,selection_tag)
{let ids=window.guiListSelections.getSelectionFromCurrentPage(elements);return goToMultiAction(ids,action,selection_tag)}
function addToParentsAndGoUp(item_ids,selection_tag)
{return $.when(changeSubItemsInParent('POST',item_ids)).done(function(data)
{window.guiListSelections.setSelection(selection_tag,item_ids,false);vstGO(getUrlBasePathDirectToPage());}).fail(function(e)
{webGui.showErrors(e)}).promise();}
function changeSubItemsInParent(action,item_ids)
{var def=new $.Deferred();if(!item_ids||item_ids.length==0)
{def.resolve()
return def.promise();}
let parent_id=spajs.urlInfo.data.reg.parent_id
let parent_type=spajs.urlInfo.data.reg.parent_type
let item_type=spajs.urlInfo.data.reg.page_type
if(!parent_id)
{console.error("Error parent_id not found")
debugger;def.resolve()
return def.promise();}
let query=[]
for(let i in item_ids){if(action=="DELETE"){let data_type=[parent_type,parent_id/1,item_type,item_ids[i]/1];query.push({type:"mod",data_type:data_type,method:action,})}
else{let data={id:item_ids[i]/1,};query.push({type:"mod",data_type:item_type,item:parent_type,data:data,pk:parent_id,method:action,})}}
return api.query(query)}
function getUrlBasePath()
{return window.location.hash.replace(/^#/,"").replace(/\/+$/,"")}
function getUrlBasePathDirectToPage()
{let api_path=spajs.urlInfo.data.reg.getApiPath();let url_vars={};for(let item in api_path.url){if(item.indexOf("api_")==0&&!isNaN(Number(api_path.url[item]))){url_vars[item]=api_path.url[item];}
if(item.indexOf("api_")==0&&isNaN(Number(api_path.url[item]))){url_vars[item]=api_path.url[item][0]=='@'?api_path.url[item]:"@"+api_path.url[item];}}
return vstMakeLocalApiUrl(api_path.api.path,url_vars).replace(/^\/|\/$/g,'');}
function renderErrorAsPage(error)
{return spajs.just.render('error_as_page',{error:error,opt:{}});}
function isEmptyObject(obj)
{if(!obj)
{return true;}
return Object.keys(obj).length==0}
function questionForAllSelectedOrNot(selection_tag,path){var answer;var action=guiSchema.path[path];if(action)
{var question="Apply action <b>'"+action.name+"'</b> for elements only from this page or for all selected elements?";var answer_buttons=["For this page's selected","For all selected"];$.when(guiPopUp.question(question,answer_buttons)).done(function(data){answer=data;if($.inArray(answer,answer_buttons)!=-1)
{if(answer==answer_buttons[0])
{goToMultiActionFromElements($('.multiple-select .item-row.selected'),action,selection_tag);}
else
{goToMultiAction(window.guiListSelections.getSelection(selection_tag),action,selection_tag);}}});}
return false;}
function questionDeleteAllSelectedOrNot(thisObj){var answer;var question="Apply action <b> 'delete' </b> for elements only from this page or for all selected elements?";var answer_buttons=["For this page's selected","For all selected"];$.when(guiPopUp.question(question,answer_buttons)).done(function(data){answer=data;if($.inArray(answer,answer_buttons)!=-1)
{let ids;let tag=thisObj.api.selectionTag;if(answer==answer_buttons[0])
{ids=window.guiListSelections.getSelectionFromCurrentPage($('.multiple-select .item-row.selected'));deleteSelectedElements(thisObj,ids,tag);}
else
{ids=window.guiListSelections.getSelection(tag);deleteSelectedElements(thisObj,ids,tag);}}});return false;}
function questionDeleteOrRemove(thisObj)
{var answer;var question="<b> Delete </b> selected elements at all or just <b> remove </b> them from this list?";var answer_buttons=["Delete this page's selected","Delete all selected","Remove this page's selected","Remove all selected"];$.when(guiPopUp.question(question,answer_buttons)).done(function(data){answer=data;if($.inArray(answer,answer_buttons)!=-1)
{let ids;let tag=thisObj.api.selectionTag;switch(answer)
{case answer_buttons[0]:ids=window.guiListSelections.getSelectionFromCurrentPage($('.multiple-select .item-row.selected'));deleteSelectedElements(thisObj,ids,tag);break;case answer_buttons[1]:ids=window.guiListSelections.getSelection(tag);deleteSelectedElements(thisObj,ids,tag);break;case answer_buttons[2]:ids=window.guiListSelections.getSelectionFromCurrentPage($('.multiple-select .item-row.selected'));removeSelectedElements(ids,tag);break;case answer_buttons[3]:ids=window.guiListSelections.getSelection(tag);removeSelectedElements(ids,tag);break;}}});return false;}
function deleteSelectedElements(thisObj,ids,tag)
{$.when(thisObj.deleteArray(ids)).done(function(d)
{window.guiListSelections.unSelectAll(tag);for(let i in ids)
{$(".item-row.item-"+ids[i]).remove();thisObj.model.data.count--;}
if($(".item-row").length==0&&thisObj.model.data.count==0)
{$("#content-section .card-body").html(spajs.just.render('items_empty_list',{}));}});return false;}
function removeSelectedElements(ids,tag)
{$.when(changeSubItemsInParent('DELETE',ids)).done(function()
{window.guiListSelections.unSelectAll(tag);for(let i in ids)
{$(".item-row.item-"+ids[i]).remove();}
guiPopUp.success("Selected elements were successfully removed from parent's list.");}).fail(function(e)
{webGui.showErrors(e)
debugger;})
return false;}
function selectPrefetchFieldsFromSchema(fields)
{let prefetch_collector={fields:{},fields_ids:{},}
for(let i in fields)
{if(fields[i].prefetch)
{prefetch_collector.fields[fields[i].name]=$.extend(true,{},fields[i].prefetch);prefetch_collector.fields_ids[fields[i].name]={};}}
return prefetch_collector;}
function selectIdsOfPrefetchFields(dataFromApi,prefetch_collector)
{for(let field in dataFromApi)
{if(prefetch_collector.fields[field])
{if(!prefetch_collector.fields_ids.hasOwnProperty(field))
{prefetch_collector.fields_ids[field]={};}
let path=prefetch_collector.fields[field].path(dataFromApi);if(path)
{if(!prefetch_collector.fields_ids[field].hasOwnProperty(path))
{prefetch_collector.fields_ids[field][path]=[];}
if($.inArray(dataFromApi[field],prefetch_collector.fields_ids[field][path])==-1&&dataFromApi[field]!=null)
{prefetch_collector.fields_ids[field][path].push(dataFromApi[field]);}}}}}
function formBulkRequestForPrefetchFields(prefetch_collector)
{let bulkArr=[];let queryObj={};for(let field in prefetch_collector.fields_ids)
{for(let path in prefetch_collector.fields_ids[field])
{let path_parts=path.replace(/^\/|\/$/g,'').split('/');if(path_parts.length>2&&!isNaN(Number(path_parts[1]))){queryObj={type:"mod",item:path_parts[0],pk:path_parts[1],data_type:path_parts.slice(2),method:"get",}}
else{let bulk_name=path.replace(/\{[A-z]+\}\/$/,"").toLowerCase().match(/\/([A-z0-9]+)\/$/);queryObj={type:"mod",item:bulk_name[1],filters:"id="+prefetch_collector.fields_ids[field][path].join(","),method:"get",}}
bulkArr.push(queryObj);}}
return bulkArr;}
function addPrefetchInfoToDataFromApi(d,dataFromApi,prefetch_collector)
{for(let field in dataFromApi)
{if(prefetch_collector.fields[field])
{let path=prefetch_collector.fields[field].path(dataFromApi);if(path){let path_parts=path.replace(/^\/|\/$/g,'').split('/');if(path_parts.length>2){addPrefetchInfoToDataFromApi_internal_level(d,dataFromApi,field,path_parts)}
else{let bulk_name=path.replace(/\{[A-z]+\}\/$/,"").toLowerCase().match(/\/([A-z0-9]+)\/$/);addPrefetchInfoToDataFromApi_second_level(d,dataFromApi,field,bulk_name)}}}}}
function addPrefetchInfoToDataFromApi_internal_level(d,dataFromApi,field,path_parts){for(var j in d){let subitem;if(d[j].subitem){subitem=d[j].subitem;}
if(typeof subitem=='string'){subitem=[subitem]}
if(d[j].item==path_parts[0]&&deepEqual(subitem,path_parts.slice(2))){let prefetch_data=d[j].data.results;for(var k in prefetch_data){if(dataFromApi[field]==prefetch_data[k].id){dataFromApi[field+'_info']=prefetch_data[k];}}}}}
function addPrefetchInfoToDataFromApi_second_level(d,dataFromApi,field,bulk_name){for(var j in d){if(d[j].item==bulk_name[1]&&d[j].subitem==null){let prefetch_data=d[j].data.results;for(var k in prefetch_data){if(dataFromApi[field]==prefetch_data[k].id){dataFromApi[field+'_info']=prefetch_data[k];}}}}}