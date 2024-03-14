import{u as V,_ as C,V as b,a as B,b as k}from"./VList.Dgr2ksud.js";import{u as w,r as v,m as F,V as A,a as E,b as L,c as N,d as O,e as $,f as S}from"./VTextField.E2T61vRU.js";import{_ as p,t as i,L as _,A as t,z as e,B as d,y as f,M as y,x as j,N as q,O as P,v as T,P as U,Q as I}from"./entry.9zux7mMk.js";import{V as h,a as x}from"./index.CcSNAF8Z.js";import{V as z}from"./VRow.DlSItuy6.js";import{V as M,_ as Q}from"./VPagination.Dvqfjc8Y.js";import{u as R}from"./index.CJeuY9gg.js";import"./VGrid.B_CvW7IJ.js";import"./VDivider.C9dgr6hG.js";import"./VContainer.B1KAAPUP.js";const G={setup(){return{v$:w(),accounts:V()}},props:{account:{type:Object,required:!1,default:{}}},data(){return{accountData:{name:"",balance:parseFloat(0).toFixed(2),...this.account},isEdit:Object.keys(this.account).length>0}},validations(){return{accountData:{name:{required:v},balance:{required:v,minValue:F(0)}}}},methods:{close(){this.$emit("close")},async submit(){this.isEdit?await this.updateAccount():await this.createAccount(),this.close()},async updateAccount(){await this.accounts.update(this.account.id,this.accountData)},async createAccount(){await this.accounts.create(this.accountData)}},computed:{isValid(){return!this.v$.accountData.$invalid}}};function H(s,a,l,u,o,c){const r=C;return i(),_($,null,{default:t(()=>[e(A,null,{default:t(()=>[d(f(o.isEdit?"Edit Account":"Create Account"),1)]),_:1}),e(E,null,{default:t(()=>[e(L,null,{default:t(()=>[e(N,{label:"Name",modelValue:o.accountData.name,"onUpdate:modelValue":a[0]||(a[0]=n=>o.accountData.name=n),onInput:u.v$.accountData.name.$touch,onBlur:u.v$.accountData.name.$touch,"error-messages":u.v$.accountData.name.$errors.map(n=>n.$message)},null,8,["modelValue","onInput","onBlur","error-messages"])]),_:1})]),_:1}),e(O,null,{default:t(()=>[e(r,{onSubmit:c.submit,onCancel:c.close,isSubmitDisabled:!c.isValid},null,8,["onSubmit","onCancel","isSubmitDisabled"])]),_:1})]),_:1})}const D=p(G,[["render",H]]),J={data(){return{overlay:!1}}};function K(s,a,l,u,o,c){const r=D;return i(),_(b,{modelValue:o.overlay,"onUpdate:modelValue":a[1]||(a[1]=n=>o.overlay=n)},{activator:t(({props:n})=>[e(h,y(n,{block:"",variant:"tonal",color:"success",size:"large"}),{default:t(()=>[d(" Create Account ")]),_:2},1040)]),default:t(({isActive:n})=>[e(z,null,{default:t(()=>[e(S,{"offset-md":"4",md:"4"},{default:t(()=>[e(r,{onClose:a[0]||(a[0]=m=>o.overlay=!o.overlay)})]),_:1})]),_:1})]),_:1},8,["modelValue"])}const W=p(J,[["render",K]]),X={setup(){return{accounts:V()}},props:{account:{type:Object,required:!0}},data(){return{dialog:!1}},methods:{async deleteAccount(){await this.accounts.delete(this.account.id)},parseBalance(s){return parseFloat(s).toFixed(2)}}},Y={class:"ml-auto"};function Z(s,a,l,u,o,c){const r=D;return i(),_($,{variant:"tonal",color:"info"},{default:t(()=>[e(A,{class:"d-flex align-center"},{default:t(()=>[d(f(l.account.name)+" ",1),j("div",Y,[e(B,{class:"mr-3",variant:"outlined"},{default:t(()=>[d(f(c.parseBalance(l.account.balance)),1)]),_:1}),e(b,{modelValue:o.dialog,"onUpdate:modelValue":a[1]||(a[1]=n=>o.dialog=n)},{activator:t(({props:n})=>[e(h,y(n,{icon:"",flat:""}),{default:t(()=>[e(x,null,{default:t(()=>[d("mdi-pencil")]),_:1})]),_:2},1040)]),default:t(({isActive:n})=>[e(r,{account:l.account,onClose:a[0]||(a[0]=m=>o.dialog=!o.dialog)},null,8,["account"])]),_:1},8,["modelValue"]),e(h,{icon:"",text:"",flat:"",class:"text-red",onClick:c.deleteAccount},{default:t(()=>[e(x,null,{default:t(()=>[d("mdi-delete")]),_:1})]),_:1},8,["onClick"])])]),_:1})]),_:1})}const tt=p(X,[["render",Z]]),et={props:{accounts:{type:Object,required:!0}},methods:{}};function at(s,a,l,u,o,c){const r=W,n=tt,m=q("auto-animate");return P((i(),_(k,{elevation:"0",class:"px-3"},{default:t(()=>[e(r),(i(!0),T(U,null,I(l.accounts,g=>(i(),_(n,{account:g,key:g.id,class:"mt-2"},null,8,["account"]))),128))]),_:1})),[[m]])}const nt=p(et,[["render",at]]),ot={setup(){return{accounts:V(),auth:R()}},data(){return{}},methods:{async fetchAccounts(){await this.accounts.getAccounts(this.auth.user.id)}},mounted(){this.fetchAccounts()},computed:{paginatorLength(){return Math.ceil(this.accounts.total/this.accounts.perPage)},page:{get(){return this.accounts.page},set(s){this.accounts.page=s,this.fetchAccounts()}}}};function ct(s,a,l,u,o,c){const r=nt,n=Q;return i(),_(n,null,{content:t(()=>[e(r,{accounts:u.accounts.accounts},null,8,["accounts"])]),pagination:t(()=>[e(M,{modelValue:c.page,"onUpdate:modelValue":a[0]||(a[0]=m=>c.page=m),length:c.paginatorLength},null,8,["modelValue","length"])]),_:1})}const st=p(ot,[["render",ct]]),Vt={__name:"accounts",setup(s){return(a,l)=>{const u=st;return i(),_(u)}}};export{Vt as default};
