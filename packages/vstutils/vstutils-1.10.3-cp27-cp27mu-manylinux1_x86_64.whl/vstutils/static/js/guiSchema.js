function openApi_guiPrepareFields(api,properties,parent_name)
{if(!guiElements)
{throw"Error not found window.guiElements"}
let fields=mergeDeep({},properties)
for(let i in fields)
{let field=fields[i]
if(!field.gui_links)
{field.gui_links=[]}
if(!field.definition)
{field.definition={}}
field.name=i
if((field.enum)&&!field.format)
{field.format="enum"}
let def_name=getObjectNameBySchema(field,1)
if(def_name)
{let def_obj=getObjectDefinitionByName(api,def_name,parent_name+"_"+i)
if(!def_obj)
{console.error("can not found definition for object "+def_name)
continue;}
field=mergeDeep(field,def_obj);if(!field.gui_links)
{field.gui_links=[]}
let format=def_name.replace("#/","").split(/\//)
if(format[1]!="Data")
{field.readOnly=true}
field.format="api"+format[1]
if(!window.guiElements[field.format])
{field.api_original_format=field.format
field.format="apiObject"}
field.definition_ref=def_name
field.gui_links.push({prop_name:'definition',list_name:'list',type:'list',$ref:def_name})
field.gui_links.push({prop_name:'definition',list_name:'page',type:'page',$ref:def_name})}
if(field.format)
{field.format=field.format.replace(/\-/g,"_")}
if(parent_name)
{try{field.parent_name_format=parent_name.replace(/\-/g,"_")+"_"+field.name}catch(exception){debugger;}}
let fieldObj;if(field.format&&window.guiElements[field.format])
{fieldObj=window.guiElements[field.format]}
else if(field.type&&window.guiElements[field.type])
{fieldObj=window.guiElements[field.type]}
if(fieldObj&&fieldObj.prepareProperties)
{field=fieldObj.prepareProperties(field)}
fields[i]=field}
return fields}
function openApi_guiPrepareFilters(schema)
{let filters=jQuery.extend(true,{},schema.filters);for(let i in schema.responses)
{if(i/1>=200&&i/1<400)
{let val=schema.responses[i]
if(val.schema&&val.schema.properties&&val.schema.properties.next&&val.schema.properties.previous)
{for(let j in filters)
{if(filters[j].name=="limit"||filters[j].name=="offset")
{delete filters[j]}}
break;}}}
return filters}
function openApi_findParentByDefinitionAndSublinks(api_obj,definition,type='list')
{for(let sub_link in api_obj.sublinks)
{let list_obj=openApi_findParentByDefinition(api_obj.sublinks[sub_link],definition,type)
if(list_obj)
{return list_obj;}}
if(api_obj.parent)
{return openApi_findParentByDefinitionAndSublinks(api_obj.parent,definition,type);}}
function openApi_findParentByDefinition(api_obj,definition,type='list')
{if(api_obj.type==type&&type=='list')
{try{let schema=api_obj.schema.list.responses[200].schema.definition_ref
if(schema==definition)
{return api_obj;}}catch(e){debugger;}}
if(api_obj.type==type&&type=='page'&&api_obj.page&&api_obj.page.api.get)
{try{let schema=api_obj.schema.get.responses[200].schema.definition_ref
if(schema==definition)
{return api_obj;}}catch(e){}
try{let schema=api_obj.schema.edit.responses[200].schema.definition_ref
if(schema==definition)
{return api_obj;}}catch(e){}}
return false}
function openApi_guiPrepareAdditionalProperties(path_schema,api_obj,fields)
{for(let i in fields)
{if(!fields[i].gui_links)
{continue;}
for(let l in fields[i].gui_links)
{let field=fields[i]
let link_type=field.gui_links[l]
let definition=link_type.$ref
if(!api_obj.parent)
{continue;}
if(field[link_type.prop_name]===undefined)
{field[link_type.prop_name]={}}
field[link_type.prop_name][link_type.list_name]=undefined
let list_obj=undefined
if(!list_obj)
{list_obj=openApi_findParentByDefinitionAndSublinks(api_obj,definition,link_type.type)}
if(!list_obj)
{for(let p in path_schema)
{if(path_schema[p].level>2||!path_schema[p].api.get)
{continue;}
let schema=getObjectNameBySchema(path_schema[p].api.get)
if(schema!=definition)
{continue;}
list_obj=path_schema[p]
break;}}
if(list_obj)
{if(link_type.type=='page'&&list_obj.type=='list'&&list_obj.page)
{list_obj=list_obj.page}
if(link_type.type=='list'&&list_obj.type=='page'&&list_obj.list)
{list_obj=list_obj.list}
field[link_type.prop_name][link_type.list_name]=list_obj
field[link_type.prop_name]["__link__"+link_type.list_name]=list_obj.path
continue;}}}
return fields}
function openApi_guiQuerySchema(api,QuerySchema,type,parent_name)
{if(!QuerySchema)
{return undefined}
let def_name=undefined
let query_schema=mergeDeep({},QuerySchema)
if(type=='get')
{if(query_schema.parameters)
{query_schema.filters=query_schema.parameters
query_schema.filters=openApi_guiPrepareFilters(query_schema)}
def_name=getObjectNameBySchema(query_schema)}
else
{if(query_schema.parameters)
{query_schema.fields=query_schema.parameters}
def_name=getObjectNameBySchema(query_schema.fields)}
delete query_schema.parameters;if(!def_name)
{return query_schema;}
let def_obj=getObjectDefinitionByName(api,def_name)
if(!def_obj)
{return query_schema;}
query_schema.fields=openApi_guiPrepareFields(api,def_obj.properties,parent_name)
for(let i in query_schema.fields)
{query_schema.fields[i].name=i}
let responses={}
for(let i in query_schema.responses)
{let resp=query_schema.responses[i]
responses[i]={description:resp.description}
let responses_def_name=getObjectNameBySchema(resp)
if(!responses_def_name)
{continue;}
let responses_def_obj=getObjectDefinitionByName(api,responses_def_name)
if(!responses_def_obj)
{throw"Not found Definition for name="+responses_def_name}
responses[i].schema=responses_def_obj}
query_schema.responses=responses
return query_schema;}
function openApi_guiSchemaSetRequiredFlags(api)
{for(let i in api.definitions)
{let definition=api.definitions[i]
if(definition.required)
{for(let j in definition.required)
{definition.properties[definition.required[j]].required=true}}}
return api}
function openApi_guiSchema(api)
{let path_schema={}
let short_schema={}
api=openApi_guiSchemaSetRequiredFlags(api)
for(let i in api.paths)
{let val=api.paths[i]
let urlLevel=(i.match(/\//g)||[]).length
let type=undefined
if(val.get)
{if(/_(get)$/.test(val.get.operationId))
{type='page'}
else if(/_list$/.test(val.get.operationId))
{type='list'}
else
{type='page'}}
else
{type='action'}
let name=i.replace(/\/{[A-z]+}/g,"").split(/\//g)
name=name[name.length-2]
path_schema[i]={level:urlLevel,path:i,type:type,name:name,bulk_name:name,name_field:'name',autoupdate:true,api:{get:openApi_guiQuerySchema(api,val.get,'get',name),patch:openApi_guiQuerySchema(api,val.patch,'patch',name),put:openApi_guiQuerySchema(api,val.put,'put',name),post:openApi_guiQuerySchema(api,val.post,'post',name),delete:openApi_guiQuerySchema(api,val.delete,'delete',name),},method:{'get':'','patch':'','put':'','post':'','delete':''},buttons:[],short_name:undefined,hide_non_required:guiLocalSettings.get('hide_non_required'),extension_class_name:["gui_"+i.replace(/\/{[A-z]+}/g,"").replace(/^\/|\/$/g,"").replace(/\//g,"_")],methodEdit:undefined,selectionTag:i.replace(/[^A-z0-9\-]/img,"_"),}
if(type!='action')
{let short_key=i.replace(/\/{[A-z]+}/g,"").replace(/^\/|\/$/g,"")
if(!short_schema[short_key])
{short_schema[short_key]={}}
short_schema[short_key][type]=path_schema[i]
path_schema[i].short_name=short_key}}
for(let path in path_schema)
{let val=path_schema[path]
let key=path.replace(/\/{[A-z]+}/g,"").split(/\//g)
key=key[key.length-2]
if(val.type=='list')
{val.methodAdd='post'
val.canAdd=false
val.canRemove=false
if(path_schema['/'+key+'/']&&val.level>2)
{if(val.api.post!=undefined)
{val.canAdd=true
val.shortestURL='/'+key+'/'}
val.canRemove=val.api.post!=undefined}
val.canCreate=val.api.post!=undefined}
else if(val.type=='page')
{val.canDelete=val.api.delete!=undefined
val.methodDelete='delete'
if(val.api.patch!=undefined)
{val.methodEdit='patch'}
if(val.api.put!=undefined)
{val.methodEdit='put'}
val.canEdit=val.methodEdit!=undefined;}}
for(let path in path_schema)
{let val=path_schema[path]
val.schema={}
if(val.type=='list')
{val.schema.list={fields:openApi_guiPrepareFields(api,val.api.get.fields,val.name),filters:val.api.get.filters,query_type:'get',operationId:val.api.get.operationId,responses:val.api.get.responses,}
val.method['get']='list'
if(val.api.post)
{val.schema.new={fields:openApi_guiPrepareFields(api,val.api.post.fields,val.name),filters:val.api.post.filters,query_type:'post',operationId:val.api.post.operationId,responses:val.api.post.responses,}
val.method['post']='new'}}
else if(val.type=='page')
{val.schema.get={fields:openApi_guiPrepareFields(api,val.api.get.fields,val.name),filters:val.api.get.filters,query_type:'get',operationId:val.api.get.operationId,responses:val.api.get.responses,}
val.method['get']='page'
for(let f in val.schema.get.fields)
{val.schema.get.fields[f].readOnly=true}
if(val.api.put)
{val.schema.edit={fields:openApi_guiPrepareFields(api,val.api.put.fields,val.name),filters:val.api.put.filters,query_type:'put',operationId:val.api.put.operationId,responses:val.api.put.responses,}
val.method['put']='edit'}
if(val.api.patch)
{val.schema.edit={fields:openApi_guiPrepareFields(api,val.api.patch.fields,val.name),filters:val.api.patch.filters,query_type:'patch',operationId:val.api.patch.operationId,responses:val.api.patch.responses,}
val.method['patch']='edit'}
if(val.api.delete)
{val.schema.delete={fields:openApi_guiPrepareFields(api,val.api.delete.fields,val.name),filters:val.api.delete.filters,query_type:'delete',operationId:val.api.delete.operationId,responses:val.api.delete.responses,}
val.method['delete']='delete'}}
else
{let query_types=['post','put','delete','patch']
for(let q in query_types)
{if(val.api[query_types[q]])
{let fields=openApi_guiPrepareFields(api,val.api[query_types[q]].fields,val.name)
val.schema.exec={fields:fields,filters:val.api[query_types[q]].filters,query_type:query_types[q],operationId:val.api[query_types[q]].operationId,responses:val.api[query_types[q]].responses,}
val.methodExec=query_types[q]
if(Object.keys(fields).length==0){val.isEmptyAction=true;}
val.method[query_types[q]]='exec'
break;}}}}
for(let path in path_schema)
{let val=path_schema[path]
if(val.type=='page')
{let list_path=path.replace(/\{[A-z]+\}\/$/,"")
if(path_schema[list_path])
{val.__link__list=list_path
val.list=path_schema[list_path]
val.list_path=list_path
path_schema[list_path].page=val
path_schema[list_path].__link__page=path
path_schema[list_path].page_path=path}}}
for(let path in path_schema)
{let val=path_schema[path]
val.sublinks=openApi_get_internal_links(path_schema,path,1)
val.sublinks_l2=openApi_get_internal_links(path_schema,path,2)
val.actions={}
val.links={}
for(let subpage in val.sublinks)
{let subobj=val.sublinks[subpage]
if(!subobj.name)
{continue;}
if(subobj.type!='action')
{val.links[subobj.name]=subobj
continue;}
val.actions[subobj.name]=subobj}
val.multi_actions={}
if(val.type=='list'&&val.page&&(val.canRemove||val.page.canDelete))
{val['multi_actions']['delete']={name:"delete",__func__onClick:'multi_action_delete',};}}
for(let path in path_schema)
{openApi_set_parents_links(path_schema,path,path_schema[path])}
for(let path in path_schema)
{let val=path_schema[path]
for(let schema in path_schema[path].schema)
{val.schema[schema].fields=openApi_guiPrepareAdditionalProperties(path_schema,val,val.schema[schema].fields)}}
for(let path in path_schema)
{delete path_schema[path].api}
let schema={path:path_schema,object:short_schema}
emitSchemaPathSignals(schema.path,"gui.schema.");return schema;}
function emitSchemaPathSignals(path_schema,prefix="openapi.schema.")
{for(let path in path_schema)
{let val=path_schema[path]
tabSignal.emit(prefix+"name."+val.name,{paths:path_schema,path:path,value:val});tabSignal.emit(prefix+"type."+val.type,{paths:path_schema,path:path,value:val});for(let schema in val.schema)
{tabSignal.emit(prefix+"name."+val.name+"."+schema,{paths:path_schema,path:path,value:val.schema[schema],schema:schema});tabSignal.emit(prefix+"schema",{paths:path_schema,path:path,value:val.schema[schema]});tabSignal.emit(prefix+"schema."+schema,{paths:path_schema,path:path,value:val.schema[schema],schema:schema});tabSignal.emit(prefix+"fields",{paths:path_schema,path:path,value:val.schema[schema],schema:schema,fields:val.schema[schema].fields});}}}
function multi_action_delete()
{if(this.api.canRemove)
{return questionDeleteOrRemove(this);}
else
{return questionDeleteAllSelectedOrNot(this);}}
function openApi_guiPagesBySchema(schema)
{for(let i in schema.path)
{let val=schema.path[i]
if(val.type=='list')
{openApi_add_list_page_path(val)}
if(val.type=='page')
{openApi_add_one_page_path(val)}
if(val.type=='action')
{openApi_add_one_action_page_path(val)}}}
function getObjectDefinitionByName(api,name,parent_name)
{if(!name||!name.replace)
{return;}
let path=name.replace("#/","").split(/\//)
let definition=path[path.length-1]
let obj=undefined
if(definition=="Data")
{if(parent_name)
{obj={properties:{},format:"api_"+parent_name,type:"object",}}}
obj=jQuery.extend(true,{},api.definitions[definition])
obj.definition_name=definition
obj.definition_ref=name
if(obj.required)
{for(let j in obj.required)
{obj.properties[obj.required[j]].required=true}}
tabSignal.emit("openapi.schema.definition",{definition:obj,api:api,name:name,parent_name:parent_name});tabSignal.emit("openapi.schema.definition."+definition,{definition:obj,name:name,parent_name:parent_name});return obj}
function getObjectNameBySchema(obj,max_level=0,level=0)
{if(!obj)
{return undefined;}
if(max_level&&max_level<=level)
{return undefined;}
if(typeof obj=='string')
{var name=obj.match(/\/([A-z0-9]+)$/)
if(name&&name[1])
{return obj[i]}
return undefined;}
if(typeof obj!='object')
{return undefined;}
for(var i in obj)
{if(i=='$ref'||i=="definition_ref")
{var name=obj[i].match(/\/([A-z0-9]+)$/)
if(name&&name[1])
{return obj[i]}}
if(typeof obj[i]=='object')
{let api_obj=getObjectNameBySchema(obj[i],max_level,level+1)
if(api_obj)
{return api_obj;}}}
return undefined;}
function getFunctionNameBySchema(obj,pattern,callback,max_level=0,level=0,path="",objects=[])
{if(!obj)
{return undefined;}
if(level>20)
{console.warn(obj,pattern,max_level,level)
debugger;throw"Error level > "+level}
if(max_level&&max_level<=level)
{debugger;return undefined;}
if(typeof obj=='string')
{return undefined;}
if(typeof obj!='object')
{return undefined;}
for(var i in obj)
{if(i=="undefined")
{debugger;}
if(i.indexOf(pattern)==0)
{obj[i.replace(pattern,'')]=callback(obj,i,pattern)
objects.push(path+"['"+i+"']")}
if(typeof obj[i]=='object')
{if(obj["__link__"+i])
{}
else
{getFunctionNameBySchema(obj[i],pattern,callback,max_level,level+1,""+path+"['"+i+"']",objects)}}}
return objects;}
function openApi_get_internal_links(paths,base_path,targetLevel)
{var res={}
for(var api_action_path in paths)
{var api_path_value=paths[api_action_path]
if(api_action_path.indexOf(base_path)!=0)
{continue;}
let dif=api_action_path.match(/\//g).length-base_path.match(/\//g).length;if(dif!=targetLevel)
{continue;}
var name=api_action_path.match(/\/([A-z0-9]+)\/$/)
if(!name)
{continue;}
res[name[1]]=api_path_value
res["__link__"+name[1]]=api_action_path}
return res;}
function openApi_set_parents_links(paths,base_path,parent_obj)
{for(var api_action_path in paths)
{var api_path_value=paths[api_action_path]
if(api_action_path.indexOf(base_path)!=0)
{continue;}
let dif=api_action_path.match(/\//g).length-base_path.match(/\//g).length;if(dif!=1)
{continue;}
api_path_value.parent=parent_obj
api_path_value.__link__parent=parent_obj.path
api_path_value.parent_path=parent_obj.path}}
function findPath(paths,base_path,value_name,replace_part="_id")
{let regexp=new RegExp(replace_part+"$","");value_name=value_name.replace(regexp,"");let path_array=base_path.split("/");do{if(paths[path_array.join("/")+value_name+"/"])
{return path_array.join("/")+value_name+"/"}
else if(path_array.length<=2)
{return false;}
path_array.splice(path_array.length-2,1);}while(1)}
function findFunctionByName(field,prefix)
{let func_name=field;if(prefix)
{func_name=field.replace(prefix,'');}
return window[func_name];}
function setDefaultPrefetchFunctions(obj)
{for(let i in obj.fields)
{if(obj.fields[i].prefetch)
{let field=obj.fields[i]
if(typeof field.prefetch=="function")
{continue;}
if(typeof field.prefetch=="object")
{if(field.prefetch.path&&typeof field.prefetch.path=="function")
{continue;}}
let prefetch_path=undefined
if(typeof field.prefetch=="string")
{if(field.prefetch.indexOf('__func__')==0)
{field.prefetch=findFunctionByName(field.prefetch,'__func__');continue;}
prefetch_path=field.prefetch.toLowerCase()
if(!obj.paths[prefetch_path])
{throw"Error in prefetch_path="+prefetch_path+" field="+JSON.stringify(field)}
obj.fields[i].prefetch={path:function(path){return function(obj){return path;}}(prefetch_path),}
continue;}
else
{prefetch_path=i.toLowerCase()}
if(!prefetch_path)
{continue;}
prefetch_path=findPath(obj.paths,obj.path,prefetch_path.replace(/_id$/,""))
if(!obj.paths[prefetch_path])
{continue;}
if(typeof obj.fields[i].prefetch!="object"){obj.fields[i].prefetch={};}
obj.fields[i].prefetch.path=function(path){return function(obj){return path;}}(prefetch_path);}}}
tabSignal.connect("openapi.schema.fields",function(obj)
{setDefaultPrefetchFunctions.apply(this,arguments)})
tabSignal.connect("openapi.schema.schema",function(obj)
{for(let i in obj.value.responses){if(obj.value.responses[i].schema){for(let k in obj.value.responses[i].schema.properties){if(obj.value.responses[i].schema.properties[k].additionalProperties)
{if(!obj.value.responses[i].schema.redirect_path&&!obj.value.responses[i].schema.redirect_field){if(obj.value.responses[i].schema.properties[k].additionalProperties.redirect){obj.value.responses[i].schema.redirect_path=findPath(obj.paths,obj.path,k);obj.value.responses[i].schema.redirect_field=k;break;}
else if(!obj.value.responses[i].schema.properties[k].additionalProperties.redirect){let redirect_path=obj.path.split("/")
redirect_path.splice(redirect_path.length-2,1)
obj.value.responses[i].schema.redirect_path=redirect_path.join("/").slice(1,-1);break;}}}}}}})
tabSignal.connect("openapi.schema.type.action",function(obj){let actionResponseDefName;try{for(let i in obj.value.schema.exec.responses){if(i>=200&&i<400&&obj.value.schema.exec.responses[i].schema){try{actionResponseDefName=obj.value.schema.exec.responses[i];break;}catch(e){}}}}catch(e)
{console.warn("Action "+obj.value.name+" don't have schema")
return;}
if(!actionResponseDefName)
{console.warn("Action "+obj.value.name+" don't have response definition")
return;}
let test=function(responses,path)
{for(let i in responses)
{let resp=responses[i]
if(i>=200&&i<400&&resp.schema){if(resp.schema.definition_name==actionResponseDefName.schema.definition_name)
{actionResponseDefName.schema.redirect_path=path;actionResponseDefName.schema.redirect_field=resp.schema.properties["pk"]||resp.schema.properties["id"];return false;}}}}
try{let path=obj.value.parent.path.split("/");path.splice(path.length-2,1);test(obj.value.parent.schema.get.responses,path.join("/"))}catch(e){return;}
try{let path=obj.value.parent.path.split("/");path.splice(path.length-2,1);test(obj.value.parent.parent.schema.list.responses,path.join("/"))}catch(e){return;}
return;})