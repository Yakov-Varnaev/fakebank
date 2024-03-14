import{m as z,a as J,u as N}from"./VGrid.B_CvW7IJ.js";import{a_ as ne,Z as V,aP as St,a$ as ze,g as ie,r as M,ar as Ne,e as K,H as A,aH as Ct,aF as ke,W as C,aU as H,c as f,aR as G,aC as Oe,b0 as Ie,b1 as _t,b2 as pt,b3 as wt,z as u,P as Ae,S as ve,Y as Q,a2 as Z,a5 as He,a7 as $,as as ee,ad as xt,ae as We,ah as kt,R as It,$ as De,o as Bt,ac as Fe,aY as Pt,ai as Et,M as be,b4 as Tt,au as w,X as fe,b5 as Vt,b6 as Lt,b7 as $t,a4 as F,b8 as Se,F as Rt,a1 as Me,aB as re,b9 as zt,ba as Be,a9 as Ce,af as Nt,bb as Ot,bc as Pe,O as me,N as Ge,aQ as At,aJ as Ht,bd as Wt}from"./entry.9zux7mMk.js";const je=["top","bottom"],Dt=["start","end","left","right"];function Ft(e,n){let[a,t]=e.split(" ");return t||(t=ne(je,a)?"start":ne(Dt,a)?"top":"center"),{side:Ee(a,n),align:Ee(t,n)}}function Ee(e,n){return e==="start"?n?"right":"left":e==="end"?n?"left":"right":e}function Rn(e){return{side:{center:"center",top:"bottom",bottom:"top",left:"right",right:"left"}[e.side],align:e.align}}function zn(e){return{side:e.side,align:{center:"center",top:"bottom",bottom:"top",left:"right",right:"left"}[e.align]}}function Nn(e){return{side:e.align,align:e.side}}function On(e){return ne(je,e.side)?"y":"x"}function An(e){let n=arguments.length>1&&arguments[1]!==void 0?arguments[1]:"div",a=arguments.length>2?arguments[2]:void 0;return V()({name:a??St(ze(e.replace(/__/g,"-"))),props:{tag:{type:String,default:n},...z()},setup(t,i){let{slots:s}=i;return()=>{var r;return ie(t.tag,{class:[e,t.class],style:t.style},(r=s.default)==null?void 0:r.call(s))}}})}function Mt(e){let n=arguments.length>1&&arguments[1]!==void 0?arguments[1]:"content";const a=M(),t=M();if(Ne){const i=new ResizeObserver(s=>{e==null||e(s,i),s.length&&(n==="content"?t.value=s[0].contentRect:t.value=s[0].target.getBoundingClientRect())});K(()=>{i.disconnect()}),A(a,(s,r)=>{r&&(i.unobserve(ke(r)),t.value=void 0),s&&i.observe(ke(s))},{flush:"post"})}return{resizeRef:a,contentRect:Ct(t)}}const Ue=C({border:[Boolean,Number,String]},"border");function qe(e){let n=arguments.length>1&&arguments[1]!==void 0?arguments[1]:H();return{borderClasses:f(()=>{const t=G(e)?e.value:e.border,i=[];if(t===!0||t==="")i.push(`${n}--border`);else if(typeof t=="string"||t===0)for(const s of String(t).split(" "))i.push(`border-${s}`);return i})}}const Gt=[null,"default","comfortable","compact"],Xe=C({density:{type:String,default:"default",validator:e=>Gt.includes(e)}},"density");function Ye(e){let n=arguments.length>1&&arguments[1]!==void 0?arguments[1]:H();return{densityClasses:f(()=>`${n}--density-${e.density}`)}}const Je=C({elevation:{type:[Number,String],validator(e){const n=parseInt(e);return!isNaN(n)&&n>=0&&n<=24}}},"elevation");function Ke(e){return{elevationClasses:f(()=>{const a=G(e)?e.value:e.elevation,t=[];return a==null||t.push(`elevation-${a}`),t})}}const le=C({rounded:{type:[Boolean,Number,String],default:void 0},tile:Boolean},"rounded");function oe(e){let n=arguments.length>1&&arguments[1]!==void 0?arguments[1]:H();return{roundedClasses:f(()=>{const t=G(e)?e.value:e.rounded,i=G(e)?e.value:e.tile,s=[];if(t===!0||t==="")s.push(`${n}--rounded`);else if(typeof t=="string"||t===0)for(const r of String(t).split(" "))s.push(`rounded-${r}`);else i&&s.push("rounded-0");return s})}}function _e(e){return Oe(()=>{const n=[],a={};if(e.value.background)if(Ie(e.value.background)){if(a.backgroundColor=e.value.background,!e.value.text&&_t(e.value.background)){const t=pt(e.value.background);if(t.a==null||t.a===1){const i=wt(t);a.color=i,a.caretColor=i}}}else n.push(`bg-${e.value.background}`);return e.value.text&&(Ie(e.value.text)?(a.color=e.value.text,a.caretColor=e.value.text):n.push(`text-${e.value.text}`)),{colorClasses:n,colorStyles:a}})}function ae(e,n){const a=f(()=>({text:G(e)?e.value:n?e[n]:null})),{colorClasses:t,colorStyles:i}=_e(a);return{textColorClasses:t,textColorStyles:i}}function ge(e,n){const a=f(()=>({background:G(e)?e.value:n?e[n]:null})),{colorClasses:t,colorStyles:i}=_e(a);return{backgroundColorClasses:t,backgroundColorStyles:i}}const jt=["elevated","flat","tonal","outlined","text","plain"];function Ut(e,n){return u(Ae,null,[e&&u("span",{key:"overlay",class:`${n}__overlay`},null),u("span",{key:"underlay",class:`${n}__underlay`},null)])}const Qe=C({color:String,variant:{type:String,default:"elevated",validator:e=>jt.includes(e)}},"variant");function qt(e){let n=arguments.length>1&&arguments[1]!==void 0?arguments[1]:H();const a=f(()=>{const{variant:s}=ve(e);return`${n}--variant-${s}`}),{colorClasses:t,colorStyles:i}=_e(f(()=>{const{variant:s,color:r}=ve(e);return{[["elevated","flat"].includes(s)?"background":"text"]:r}}));return{colorClasses:t,colorStyles:i,variantClasses:a}}const Ze=C({divided:Boolean,...Ue(),...z(),...Xe(),...Je(),...le(),...J(),...Q(),...Qe()},"VBtnGroup"),Te=V()({name:"VBtnGroup",props:Ze(),setup(e,n){let{slots:a}=n;const{themeClasses:t}=Z(e),{densityClasses:i}=Ye(e),{borderClasses:s}=qe(e),{elevationClasses:r}=Ke(e),{roundedClasses:l}=oe(e);He({VBtn:{height:"auto",color:$(e,"color"),density:$(e,"density"),flat:!0,variant:$(e,"variant")}}),N(()=>u(e.tag,{class:["v-btn-group",{"v-btn-group--divided":e.divided},t.value,s.value,i.value,r.value,l.value,e.class],style:e.style},a))}}),Xt=C({modelValue:{type:null,default:void 0},multiple:Boolean,mandatory:[Boolean,String],max:Number,selectedClass:String,disabled:Boolean},"group"),Yt=C({value:null,disabled:Boolean,selectedClass:String},"group-item");function Jt(e,n){let a=arguments.length>2&&arguments[2]!==void 0?arguments[2]:!0;const t=ee("useGroupItem");if(!t)throw new Error("[Vuetify] useGroupItem composable must be used inside a component setup function");const i=xt();We(Symbol.for(`${n.description}:id`),i);const s=kt(n,null);if(!s){if(!a)return s;throw new Error(`[Vuetify] Could not find useGroup injection with symbol ${n.description}`)}const r=$(e,"value"),l=f(()=>!!(s.disabled.value||e.disabled));s.register({id:i,value:r,disabled:l},t),K(()=>{s.unregister(i)});const o=f(()=>s.isSelected(i)),v=f(()=>o.value&&[s.selectedClass.value,e.selectedClass]);return A(o,m=>{t.emit("group:selected",{value:m})},{flush:"sync"}),{id:i,isSelected:o,toggle:()=>s.select(i,!o.value),select:m=>s.select(i,m),selectedClass:v,value:r,disabled:l,group:s}}function Kt(e,n){let a=!1;const t=It([]),i=De(e,"modelValue",[],d=>d==null?[]:et(t,Et(d)),d=>{const c=Zt(t,d);return e.multiple?c:c[0]}),s=ee("useGroup");function r(d,c){const S=d,y=Symbol.for(`${n.description}:id`),p=Pt(y,s==null?void 0:s.vnode).indexOf(c);ve(S.value)==null&&(S.value=p),p>-1?t.splice(p,0,S):t.push(S)}function l(d){if(a)return;o();const c=t.findIndex(S=>S.id===d);t.splice(c,1)}function o(){const d=t.find(c=>!c.disabled);d&&e.mandatory==="force"&&!i.value.length&&(i.value=[d.id])}Bt(()=>{o()}),K(()=>{a=!0});function v(d,c){const S=t.find(y=>y.id===d);if(!(c&&(S!=null&&S.disabled)))if(e.multiple){const y=i.value.slice(),k=y.findIndex(g=>g===d),p=~k;if(c=c??!p,p&&e.mandatory&&y.length<=1||!p&&e.max!=null&&y.length+1>e.max)return;k<0&&c?y.push(d):k>=0&&!c&&y.splice(k,1),i.value=y}else{const y=i.value.includes(d);if(e.mandatory&&y)return;i.value=c??!y?[d]:[]}}function m(d){if(e.multiple,i.value.length){const c=i.value[0],S=t.findIndex(p=>p.id===c);let y=(S+d)%t.length,k=t[y];for(;k.disabled&&y!==S;)y=(y+d)%t.length,k=t[y];if(k.disabled)return;i.value=[t[y].id]}else{const c=t.find(S=>!S.disabled);c&&(i.value=[c.id])}}const b={register:r,unregister:l,selected:i,select:v,disabled:$(e,"disabled"),prev:()=>m(t.length-1),next:()=>m(1),isSelected:d=>i.value.includes(d),selectedClass:f(()=>e.selectedClass),items:f(()=>t),getItemIndex:d=>Qt(t,d)};return We(n,b),b}function Qt(e,n){const a=et(e,[n]);return a.length?e.findIndex(t=>t.id===a[0]):-1}function et(e,n){const a=[];return n.forEach(t=>{const i=e.find(r=>Fe(t,r.value)),s=e[t];(i==null?void 0:i.value)!=null?a.push(i.id):s!=null&&a.push(s.id)}),a}function Zt(e,n){const a=[];return n.forEach(t=>{const i=e.findIndex(s=>s.id===t);if(~i){const s=e[i];a.push(s.value!=null?s.value:i)}}),a}const tt=Symbol.for("vuetify:v-btn-toggle"),en=C({...Ze(),...Xt()},"VBtnToggle");V()({name:"VBtnToggle",props:en(),emits:{"update:modelValue":e=>!0},setup(e,n){let{slots:a}=n;const{isSelected:t,next:i,prev:s,select:r,selected:l}=Kt(e,tt);return N(()=>{const o=Te.filterProps(e);return u(Te,be({class:["v-btn-toggle",e.class]},o,{style:e.style}),{default:()=>{var v;return[(v=a.default)==null?void 0:v.call(a,{isSelected:t,next:i,prev:s,select:r,selected:l})]}})}),{next:i,prev:s,select:r}}});const tn=C({defaults:Object,disabled:Boolean,reset:[Number,String],root:[Boolean,String],scoped:Boolean},"VDefaultsProvider"),ue=V(!1)({name:"VDefaultsProvider",props:tn(),setup(e,n){let{slots:a}=n;const{defaults:t,disabled:i,reset:s,root:r,scoped:l}=Tt(e);return He(t,{reset:s,root:r,scoped:l,disabled:i}),()=>{var o;return(o=a.default)==null?void 0:o.call(a)}}}),nn=["x-small","small","default","large","x-large"],pe=C({size:{type:[String,Number],default:"default"}},"size");function we(e){let n=arguments.length>1&&arguments[1]!==void 0?arguments[1]:H();return Oe(()=>{let a,t;return ne(nn,e.size)?a=`${n}--size-${e.size}`:e.size&&(t={width:w(e.size),height:w(e.size)}),{sizeClasses:a,sizeStyles:t}})}const an=C({color:String,start:Boolean,end:Boolean,icon:fe,...z(),...pe(),...J({tag:"i"}),...Q()},"VIcon"),ce=V()({name:"VIcon",props:an(),setup(e,n){let{attrs:a,slots:t}=n;const i=M(),{themeClasses:s}=Z(e),{iconData:r}=Vt(f(()=>i.value||e.icon)),{sizeClasses:l}=we(e),{textColorClasses:o,textColorStyles:v}=ae($(e,"color"));return N(()=>{var b,d;const m=(b=t.default)==null?void 0:b.call(t);return m&&(i.value=(d=Lt(m).filter(c=>c.type===$t&&c.children&&typeof c.children=="string")[0])==null?void 0:d.children),u(r.value.component,{tag:e.tag,icon:r.value.icon,class:["v-icon","notranslate",s.value,l.value,o.value,{"v-icon--clickable":!!a.onClick,"v-icon--start":e.start,"v-icon--end":e.end},e.class],style:[l.value?void 0:{fontSize:w(e.size),height:w(e.size),width:w(e.size)},v.value,e.style],role:a.onClick?"button":void 0,"aria-hidden":!a.onClick},{default:()=>[m]})}),{}}});function nt(e,n){const a=M(),t=F(!1);if(Se){const i=new IntersectionObserver(s=>{e==null||e(s,i),t.value=!!s.find(r=>r.isIntersecting)},n);K(()=>{i.disconnect()}),A(a,(s,r)=>{r&&(i.unobserve(r),t.value=!1),s&&i.observe(s)},{flush:"post"})}return{intersectionRef:a,isIntersecting:t}}const sn=C({bgColor:String,color:String,indeterminate:[Boolean,String],modelValue:{type:[Number,String],default:0},rotate:{type:[Number,String],default:0},width:{type:[Number,String],default:4},...z(),...pe(),...J({tag:"div"}),...Q()},"VProgressCircular"),rn=V()({name:"VProgressCircular",props:sn(),setup(e,n){let{slots:a}=n;const t=20,i=2*Math.PI*t,s=M(),{themeClasses:r}=Z(e),{sizeClasses:l,sizeStyles:o}=we(e),{textColorClasses:v,textColorStyles:m}=ae($(e,"color")),{textColorClasses:b,textColorStyles:d}=ae($(e,"bgColor")),{intersectionRef:c,isIntersecting:S}=nt(),{resizeRef:y,contentRect:k}=Mt(),p=f(()=>Math.max(0,Math.min(100,parseFloat(e.modelValue)))),g=f(()=>Number(e.width)),_=f(()=>o.value?Number(e.size):k.value?k.value.width:Math.max(g.value,32)),B=f(()=>t/(1-g.value/_.value)*2),P=f(()=>g.value/_.value*B.value),O=f(()=>w((100-p.value)/100*i));return Rt(()=>{c.value=s.value,y.value=s.value}),N(()=>u(e.tag,{ref:s,class:["v-progress-circular",{"v-progress-circular--indeterminate":!!e.indeterminate,"v-progress-circular--visible":S.value,"v-progress-circular--disable-shrink":e.indeterminate==="disable-shrink"},r.value,l.value,v.value,e.class],style:[o.value,m.value,e.style],role:"progressbar","aria-valuemin":"0","aria-valuemax":"100","aria-valuenow":e.indeterminate?void 0:p.value},{default:()=>[u("svg",{style:{transform:`rotate(calc(-90deg + ${Number(e.rotate)}deg))`},xmlns:"http://www.w3.org/2000/svg",viewBox:`0 0 ${B.value} ${B.value}`},[u("circle",{class:["v-progress-circular__underlay",b.value],style:d.value,fill:"transparent",cx:"50%",cy:"50%",r:t,"stroke-width":P.value,"stroke-dasharray":i,"stroke-dashoffset":0},null),u("circle",{class:"v-progress-circular__overlay",fill:"transparent",cx:"50%",cy:"50%",r:t,"stroke-width":P.value,"stroke-dasharray":i,"stroke-dashoffset":O.value},null)]),a.default&&u("div",{class:"v-progress-circular__content"},[a.default({value:p.value})])]})),{}}}),at=C({height:[Number,String],maxHeight:[Number,String],maxWidth:[Number,String],minHeight:[Number,String],minWidth:[Number,String],width:[Number,String]},"dimension");function st(e){return{dimensionStyles:f(()=>({height:w(e.height),maxHeight:w(e.maxHeight),maxWidth:w(e.maxWidth),minHeight:w(e.minHeight),minWidth:w(e.minWidth),width:w(e.width)}))}}const Ve={center:"center",top:"bottom",bottom:"top",left:"right",right:"left"},it=C({location:String},"location");function rt(e){let n=arguments.length>1&&arguments[1]!==void 0?arguments[1]:!1,a=arguments.length>2?arguments[2]:void 0;const{isRtl:t}=Me();return{locationStyles:f(()=>{if(!e.location)return{};const{side:s,align:r}=Ft(e.location.split(" ").length>1?e.location:`${e.location} center`,t.value);function l(v){return a?a(v):0}const o={};return s!=="center"&&(n?o[Ve[s]]=`calc(100% - ${l(s)}px)`:o[s]=0),r!=="center"?n?o[Ve[r]]=`calc(100% - ${l(r)}px)`:o[r]=0:(s==="center"?o.top=o.left="50%":o[{top:"left",bottom:"left",left:"top",right:"top"}[s]]="50%",o.transform={top:"translateX(-50%)",bottom:"translateX(-50%)",left:"translateY(-50%)",right:"translateY(-50%)",center:"translate(-50%, -50%)"}[s]),o})}}const ln=C({absolute:Boolean,active:{type:Boolean,default:!0},bgColor:String,bgOpacity:[Number,String],bufferValue:{type:[Number,String],default:0},clickable:Boolean,color:String,height:{type:[Number,String],default:4},indeterminate:Boolean,max:{type:[Number,String],default:100},modelValue:{type:[Number,String],default:0},reverse:Boolean,stream:Boolean,striped:Boolean,roundedBar:Boolean,...z(),...it({location:"top"}),...le(),...J(),...Q()},"VProgressLinear"),on=V()({name:"VProgressLinear",props:ln(),emits:{"update:modelValue":e=>!0},setup(e,n){let{slots:a}=n;const t=De(e,"modelValue"),{isRtl:i,rtlClasses:s}=Me(),{themeClasses:r}=Z(e),{locationStyles:l}=rt(e),{textColorClasses:o,textColorStyles:v}=ae(e,"color"),{backgroundColorClasses:m,backgroundColorStyles:b}=ge(f(()=>e.bgColor||e.color)),{backgroundColorClasses:d,backgroundColorStyles:c}=ge(e,"color"),{roundedClasses:S}=oe(e),{intersectionRef:y,isIntersecting:k}=nt(),p=f(()=>parseInt(e.max,10)),g=f(()=>parseInt(e.height,10)),_=f(()=>parseFloat(e.bufferValue)/p.value*100),B=f(()=>parseFloat(t.value)/p.value*100),P=f(()=>i.value!==e.reverse),O=f(()=>e.indeterminate?"fade-transition":"slide-x-transition"),W=f(()=>e.bgOpacity==null?e.bgOpacity:parseFloat(e.bgOpacity));function j(I){if(!y.value)return;const{left:R,right:D,width:h}=y.value.getBoundingClientRect(),x=P.value?h-I.clientX+(D-h):I.clientX-R;t.value=Math.round(x/h*p.value)}return N(()=>u(e.tag,{ref:y,class:["v-progress-linear",{"v-progress-linear--absolute":e.absolute,"v-progress-linear--active":e.active&&k.value,"v-progress-linear--reverse":P.value,"v-progress-linear--rounded":e.rounded,"v-progress-linear--rounded-bar":e.roundedBar,"v-progress-linear--striped":e.striped},S.value,r.value,s.value,e.class],style:[{bottom:e.location==="bottom"?0:void 0,top:e.location==="top"?0:void 0,height:e.active?w(g.value):0,"--v-progress-linear-height":w(g.value),...l.value},e.style],role:"progressbar","aria-hidden":e.active?"false":"true","aria-valuemin":"0","aria-valuemax":e.max,"aria-valuenow":e.indeterminate?void 0:B.value,onClick:e.clickable&&j},{default:()=>[e.stream&&u("div",{key:"stream",class:["v-progress-linear__stream",o.value],style:{...v.value,[P.value?"left":"right"]:w(-g.value),borderTop:`${w(g.value/2)} dotted`,opacity:W.value,top:`calc(50% - ${w(g.value/4)})`,width:w(100-_.value,"%"),"--v-progress-linear-stream-to":w(g.value*(P.value?1:-1))}},null),u("div",{class:["v-progress-linear__background",m.value],style:[b.value,{opacity:W.value,width:w(e.stream?_.value:100,"%")}]},null),u(re,{name:O.value},{default:()=>[e.indeterminate?u("div",{class:"v-progress-linear__indeterminate"},[["long","short"].map(I=>u("div",{key:I,class:["v-progress-linear__indeterminate",I,d.value],style:c.value},null))]):u("div",{class:["v-progress-linear__determinate",d.value],style:[c.value,{width:w(B.value,"%")}]},null)]}),a.default&&u("div",{class:"v-progress-linear__content"},[a.default({value:B.value,buffer:_.value})])]})),{}}}),un=C({loading:[Boolean,String]},"loader");function cn(e){let n=arguments.length>1&&arguments[1]!==void 0?arguments[1]:H();return{loaderClasses:f(()=>({[`${n}--loading`]:e.loading}))}}function Hn(e,n){var t;let{slots:a}=n;return u("div",{class:`${e.name}__loader`},[((t=a.default)==null?void 0:t.call(a,{color:e.color,isActive:e.active}))||u(on,{absolute:e.absolute,active:e.active,color:e.color,height:"2",indeterminate:!0},null)])}const dn=["static","relative","fixed","absolute","sticky"],vn=C({position:{type:String,validator:e=>dn.includes(e)}},"position");function fn(e){let n=arguments.length>1&&arguments[1]!==void 0?arguments[1]:H();return{positionClasses:f(()=>e.position?`${n}--${e.position}`:void 0)}}function mn(){const e=ee("useRoute");return f(()=>{var n;return(n=e==null?void 0:e.proxy)==null?void 0:n.$route})}function Wn(){var e,n;return(n=(e=ee("useRouter"))==null?void 0:e.proxy)==null?void 0:n.$router}function gn(e,n){const a=zt("RouterLink"),t=f(()=>!!(e.href||e.to)),i=f(()=>(t==null?void 0:t.value)||Be(n,"click")||Be(e,"click"));if(typeof a=="string")return{isLink:t,isClickable:i,href:$(e,"href")};const s=e.to?a.useLink(e):void 0,r=mn();return{isLink:t,isClickable:i,route:s==null?void 0:s.route,navigate:s==null?void 0:s.navigate,isActive:s&&f(()=>{var l,o,v;return e.exact?r.value?((v=s.isExactActive)==null?void 0:v.value)&&Fe(s.route.value.query,r.value.query):(o=s.isExactActive)==null?void 0:o.value:(l=s.isActive)==null?void 0:l.value}),href:f(()=>e.to?s==null?void 0:s.route.value.href:e.href)}}const hn=C({href:String,replace:Boolean,to:[String,Object],exact:Boolean},"router");let de=!1;function Dn(e,n){let a=!1,t,i;Ne&&(Ce(()=>{window.addEventListener("popstate",s),t=e==null?void 0:e.beforeEach((r,l,o)=>{de?a?n(o):o():setTimeout(()=>a?n(o):o()),de=!0}),i=e==null?void 0:e.afterEach(()=>{de=!1})}),Nt(()=>{window.removeEventListener("popstate",s),t==null||t(),i==null||i()}));function s(r){var l;(l=r.state)!=null&&l.replaced||(a=!0,setTimeout(()=>a=!1))}}function yn(e,n){A(()=>{var a;return(a=e.isActive)==null?void 0:a.value},a=>{e.isLink.value&&a&&n&&Ce(()=>{n(!0)})},{immediate:!0})}const he=Symbol("rippleStop"),bn=80;function Le(e,n){e.style.transform=n,e.style.webkitTransform=n}function ye(e){return e.constructor.name==="TouchEvent"}function lt(e){return e.constructor.name==="KeyboardEvent"}const Sn=function(e,n){var b;let a=arguments.length>2&&arguments[2]!==void 0?arguments[2]:{},t=0,i=0;if(!lt(e)){const d=n.getBoundingClientRect(),c=ye(e)?e.touches[e.touches.length-1]:e;t=c.clientX-d.left,i=c.clientY-d.top}let s=0,r=.3;(b=n._ripple)!=null&&b.circle?(r=.15,s=n.clientWidth/2,s=a.center?s:s+Math.sqrt((t-s)**2+(i-s)**2)/4):s=Math.sqrt(n.clientWidth**2+n.clientHeight**2)/2;const l=`${(n.clientWidth-s*2)/2}px`,o=`${(n.clientHeight-s*2)/2}px`,v=a.center?l:`${t-s}px`,m=a.center?o:`${i-s}px`;return{radius:s,scale:r,x:v,y:m,centerX:l,centerY:o}},se={show(e,n){var c;let a=arguments.length>2&&arguments[2]!==void 0?arguments[2]:{};if(!((c=n==null?void 0:n._ripple)!=null&&c.enabled))return;const t=document.createElement("span"),i=document.createElement("span");t.appendChild(i),t.className="v-ripple__container",a.class&&(t.className+=` ${a.class}`);const{radius:s,scale:r,x:l,y:o,centerX:v,centerY:m}=Sn(e,n,a),b=`${s*2}px`;i.className="v-ripple__animation",i.style.width=b,i.style.height=b,n.appendChild(t);const d=window.getComputedStyle(n);d&&d.position==="static"&&(n.style.position="relative",n.dataset.previousPosition="static"),i.classList.add("v-ripple__animation--enter"),i.classList.add("v-ripple__animation--visible"),Le(i,`translate(${l}, ${o}) scale3d(${r},${r},${r})`),i.dataset.activated=String(performance.now()),setTimeout(()=>{i.classList.remove("v-ripple__animation--enter"),i.classList.add("v-ripple__animation--in"),Le(i,`translate(${v}, ${m}) scale3d(1,1,1)`)},0)},hide(e){var s;if(!((s=e==null?void 0:e._ripple)!=null&&s.enabled))return;const n=e.getElementsByClassName("v-ripple__animation");if(n.length===0)return;const a=n[n.length-1];if(a.dataset.isHiding)return;a.dataset.isHiding="true";const t=performance.now()-Number(a.dataset.activated),i=Math.max(250-t,0);setTimeout(()=>{a.classList.remove("v-ripple__animation--in"),a.classList.add("v-ripple__animation--out"),setTimeout(()=>{var l;e.getElementsByClassName("v-ripple__animation").length===1&&e.dataset.previousPosition&&(e.style.position=e.dataset.previousPosition,delete e.dataset.previousPosition),((l=a.parentNode)==null?void 0:l.parentNode)===e&&e.removeChild(a.parentNode)},300)},i)}};function ot(e){return typeof e>"u"||!!e}function X(e){const n={},a=e.currentTarget;if(!(!(a!=null&&a._ripple)||a._ripple.touched||e[he])){if(e[he]=!0,ye(e))a._ripple.touched=!0,a._ripple.isTouch=!0;else if(a._ripple.isTouch)return;if(n.center=a._ripple.centered||lt(e),a._ripple.class&&(n.class=a._ripple.class),ye(e)){if(a._ripple.showTimerCommit)return;a._ripple.showTimerCommit=()=>{se.show(e,a,n)},a._ripple.showTimer=window.setTimeout(()=>{var t;(t=a==null?void 0:a._ripple)!=null&&t.showTimerCommit&&(a._ripple.showTimerCommit(),a._ripple.showTimerCommit=null)},bn)}else se.show(e,a,n)}}function $e(e){e[he]=!0}function E(e){const n=e.currentTarget;if(n!=null&&n._ripple){if(window.clearTimeout(n._ripple.showTimer),e.type==="touchend"&&n._ripple.showTimerCommit){n._ripple.showTimerCommit(),n._ripple.showTimerCommit=null,n._ripple.showTimer=window.setTimeout(()=>{E(e)});return}window.setTimeout(()=>{n._ripple&&(n._ripple.touched=!1)}),se.hide(n)}}function ut(e){const n=e.currentTarget;n!=null&&n._ripple&&(n._ripple.showTimerCommit&&(n._ripple.showTimerCommit=null),window.clearTimeout(n._ripple.showTimer))}let Y=!1;function ct(e){!Y&&(e.keyCode===Pe.enter||e.keyCode===Pe.space)&&(Y=!0,X(e))}function dt(e){Y=!1,E(e)}function vt(e){Y&&(Y=!1,E(e))}function ft(e,n,a){const{value:t,modifiers:i}=n,s=ot(t);if(s||se.hide(e),e._ripple=e._ripple??{},e._ripple.enabled=s,e._ripple.centered=i.center,e._ripple.circle=i.circle,Ot(t)&&t.class&&(e._ripple.class=t.class),s&&!a){if(i.stop){e.addEventListener("touchstart",$e,{passive:!0}),e.addEventListener("mousedown",$e);return}e.addEventListener("touchstart",X,{passive:!0}),e.addEventListener("touchend",E,{passive:!0}),e.addEventListener("touchmove",ut,{passive:!0}),e.addEventListener("touchcancel",E),e.addEventListener("mousedown",X),e.addEventListener("mouseup",E),e.addEventListener("mouseleave",E),e.addEventListener("keydown",ct),e.addEventListener("keyup",dt),e.addEventListener("blur",vt),e.addEventListener("dragstart",E,{passive:!0})}else!s&&a&&mt(e)}function mt(e){e.removeEventListener("mousedown",X),e.removeEventListener("touchstart",X),e.removeEventListener("touchend",E),e.removeEventListener("touchmove",ut),e.removeEventListener("touchcancel",E),e.removeEventListener("mouseup",E),e.removeEventListener("mouseleave",E),e.removeEventListener("keydown",ct),e.removeEventListener("keyup",dt),e.removeEventListener("dragstart",E),e.removeEventListener("blur",vt)}function Cn(e,n){ft(e,n,!1)}function _n(e){delete e._ripple,mt(e)}function pn(e,n){if(n.value===n.oldValue)return;const a=ot(n.oldValue);ft(e,n,a)}const wn={mounted:Cn,unmounted:_n,updated:pn},xn=C({active:{type:Boolean,default:void 0},symbol:{type:null,default:tt},flat:Boolean,icon:[Boolean,String,Function,Object],prependIcon:fe,appendIcon:fe,block:Boolean,slim:Boolean,stacked:Boolean,ripple:{type:[Boolean,Object],default:!0},text:String,...Ue(),...z(),...Xe(),...at(),...Je(),...Yt(),...un(),...it(),...vn(),...le(),...hn(),...pe(),...J({tag:"button"}),...Q(),...Qe({variant:"elevated"})},"VBtn"),Fn=V()({name:"VBtn",directives:{Ripple:wn},props:xn(),emits:{"group:selected":e=>!0},setup(e,n){let{attrs:a,slots:t}=n;const{themeClasses:i}=Z(e),{borderClasses:s}=qe(e),{colorClasses:r,colorStyles:l,variantClasses:o}=qt(e),{densityClasses:v}=Ye(e),{dimensionStyles:m}=st(e),{elevationClasses:b}=Ke(e),{loaderClasses:d}=cn(e),{locationStyles:c}=rt(e),{positionClasses:S}=fn(e),{roundedClasses:y}=oe(e),{sizeClasses:k,sizeStyles:p}=we(e),g=Jt(e,e.symbol,!1),_=gn(e,a),B=f(()=>{var I;return e.active!==void 0?e.active:_.isLink.value?(I=_.isActive)==null?void 0:I.value:g==null?void 0:g.isSelected.value}),P=f(()=>(g==null?void 0:g.disabled.value)||e.disabled),O=f(()=>e.variant==="elevated"&&!(e.disabled||e.flat||e.border)),W=f(()=>{if(!(e.value===void 0||typeof e.value=="symbol"))return Object(e.value)===e.value?JSON.stringify(e.value,null,0):e.value});function j(I){var R;P.value||_.isLink.value&&(I.metaKey||I.ctrlKey||I.shiftKey||I.button!==0||a.target==="_blank")||((R=_.navigate)==null||R.call(_,I),g==null||g.toggle())}return yn(_,g==null?void 0:g.select),N(()=>{var L,U;const I=_.isLink.value?"a":e.tag,R=!!(e.prependIcon||t.prepend),D=!!(e.appendIcon||t.append),h=!!(e.icon&&e.icon!==!0),x=(g==null?void 0:g.isSelected.value)&&(!_.isLink.value||((L=_.isActive)==null?void 0:L.value))||!g||((U=_.isActive)==null?void 0:U.value);return me(u(I,{type:I==="a"?void 0:"button",class:["v-btn",g==null?void 0:g.selectedClass.value,{"v-btn--active":B.value,"v-btn--block":e.block,"v-btn--disabled":P.value,"v-btn--elevated":O.value,"v-btn--flat":e.flat,"v-btn--icon":!!e.icon,"v-btn--loading":e.loading,"v-btn--slim":e.slim,"v-btn--stacked":e.stacked},i.value,s.value,x?r.value:void 0,v.value,b.value,d.value,S.value,y.value,k.value,o.value,e.class],style:[x?l.value:void 0,m.value,c.value,p.value,e.style],disabled:P.value||void 0,href:_.href.value,onClick:j,value:W.value},{default:()=>{var q;return[Ut(!0,"v-btn"),!e.icon&&R&&u("span",{key:"prepend",class:"v-btn__prepend"},[t.prepend?u(ue,{key:"prepend-defaults",disabled:!e.prependIcon,defaults:{VIcon:{icon:e.prependIcon}}},t.prepend):u(ce,{key:"prepend-icon",icon:e.prependIcon},null)]),u("span",{class:"v-btn__content","data-no-activator":""},[!t.default&&h?u(ce,{key:"content-icon",icon:e.icon},null):u(ue,{key:"content-defaults",disabled:!h,defaults:{VIcon:{icon:e.icon}}},{default:()=>{var xe;return[((xe=t.default)==null?void 0:xe.call(t))??e.text]}})]),!e.icon&&D&&u("span",{key:"append",class:"v-btn__append"},[t.append?u(ue,{key:"append-defaults",disabled:!e.appendIcon,defaults:{VIcon:{icon:e.appendIcon}}},t.append):u(ce,{key:"append-icon",icon:e.appendIcon},null)]),!!e.loading&&u("span",{key:"loader",class:"v-btn__loader"},[((q=t.loader)==null?void 0:q.call(t))??u(rn,{color:typeof e.loading=="boolean"?void 0:e.loading,indeterminate:!0,size:"23",width:"2"},null)])]}}),[[Ge("ripple"),!P.value&&e.ripple,null]])}),{group:g}}});function kn(e){return{aspectStyles:f(()=>{const n=Number(e.aspectRatio);return n?{paddingBottom:String(1/n*100)+"%"}:void 0})}}const gt=C({aspectRatio:[String,Number],contentClass:String,inline:Boolean,...z(),...at()},"VResponsive"),Re=V()({name:"VResponsive",props:gt(),setup(e,n){let{slots:a}=n;const{aspectStyles:t}=kn(e),{dimensionStyles:i}=st(e);return N(()=>{var s;return u("div",{class:["v-responsive",{"v-responsive--inline":e.inline},e.class],style:[i.value,e.style]},[u("div",{class:"v-responsive__sizer",style:t.value},null),(s=a.additional)==null?void 0:s.call(a),a.default&&u("div",{class:["v-responsive__content",e.contentClass]},[a.default()])])}),{}}}),In=C({transition:{type:[Boolean,String,Object],default:"fade-transition",validator:e=>e!==!0}},"transition"),te=(e,n)=>{let{slots:a}=n;const{transition:t,disabled:i,...s}=e,{component:r=re,...l}=typeof t=="object"?t:{};return ie(r,be(typeof t=="string"?{name:i?"":t}:l,s,{disabled:i}),a)};function Bn(e,n){if(!Se)return;const a=n.modifiers||{},t=n.value,{handler:i,options:s}=typeof t=="object"?t:{handler:t,options:{}},r=new IntersectionObserver(function(){var b;let l=arguments.length>0&&arguments[0]!==void 0?arguments[0]:[],o=arguments.length>1?arguments[1]:void 0;const v=(b=e._observe)==null?void 0:b[n.instance.$.uid];if(!v)return;const m=l.some(d=>d.isIntersecting);i&&(!a.quiet||v.init)&&(!a.once||m||v.init)&&i(m,l,o),m&&a.once?ht(e,n):v.init=!0},s);e._observe=Object(e._observe),e._observe[n.instance.$.uid]={init:!1,observer:r},r.observe(e)}function ht(e,n){var t;const a=(t=e._observe)==null?void 0:t[n.instance.$.uid];a&&(a.observer.unobserve(e),delete e._observe[n.instance.$.uid])}const Pn={mounted:Bn,unmounted:ht},En=Pn,Tn=C({alt:String,cover:Boolean,color:String,draggable:{type:[Boolean,String],default:void 0},eager:Boolean,gradient:String,lazySrc:String,options:{type:Object,default:()=>({root:void 0,rootMargin:void 0,threshold:void 0})},sizes:String,src:{type:[String,Object],default:""},crossorigin:String,referrerpolicy:String,srcset:String,position:String,...gt(),...z(),...le(),...In()},"VImg"),Mn=V()({name:"VImg",directives:{intersect:En},props:Tn(),emits:{loadstart:e=>!0,load:e=>!0,error:e=>!0},setup(e,n){let{emit:a,slots:t}=n;const{backgroundColorClasses:i,backgroundColorStyles:s}=ge($(e,"color")),{roundedClasses:r}=oe(e),l=ee("VImg"),o=F(""),v=M(),m=F(e.eager?"loading":"idle"),b=F(),d=F(),c=f(()=>e.src&&typeof e.src=="object"?{src:e.src.src,srcset:e.srcset||e.src.srcset,lazySrc:e.lazySrc||e.src.lazySrc,aspect:Number(e.aspectRatio||e.src.aspect||0)}:{src:e.src,srcset:e.srcset,lazySrc:e.lazySrc,aspect:Number(e.aspectRatio||0)}),S=f(()=>c.value.aspect||b.value/d.value||0);A(()=>e.src,()=>{y(m.value!=="idle")}),A(S,(h,x)=>{!h&&x&&v.value&&B(v.value)}),At(()=>y());function y(h){if(!(e.eager&&h)&&!(Se&&!h&&!e.eager)){if(m.value="loading",c.value.lazySrc){const x=new Image;x.src=c.value.lazySrc,B(x,null)}c.value.src&&Ce(()=>{var x;a("loadstart",((x=v.value)==null?void 0:x.currentSrc)||c.value.src),setTimeout(()=>{var L;if(!l.isUnmounted)if((L=v.value)!=null&&L.complete){if(v.value.naturalWidth||p(),m.value==="error")return;S.value||B(v.value,null),m.value==="loading"&&k()}else S.value||B(v.value),g()})})}}function k(){var h;l.isUnmounted||(g(),B(v.value),m.value="loaded",a("load",((h=v.value)==null?void 0:h.currentSrc)||c.value.src))}function p(){var h;l.isUnmounted||(m.value="error",a("error",((h=v.value)==null?void 0:h.currentSrc)||c.value.src))}function g(){const h=v.value;h&&(o.value=h.currentSrc||h.src)}let _=-1;K(()=>{clearTimeout(_)});function B(h){let x=arguments.length>1&&arguments[1]!==void 0?arguments[1]:100;const L=()=>{if(clearTimeout(_),l.isUnmounted)return;const{naturalHeight:U,naturalWidth:q}=h;U||q?(b.value=q,d.value=U):!h.complete&&m.value==="loading"&&x!=null?_=window.setTimeout(L,x):(h.currentSrc.endsWith(".svg")||h.currentSrc.startsWith("data:image/svg+xml"))&&(b.value=1,d.value=1)};L()}const P=f(()=>({"v-img__img--cover":e.cover,"v-img__img--contain":!e.cover})),O=()=>{var L;if(!c.value.src||m.value==="idle")return null;const h=u("img",{class:["v-img__img",P.value],style:{objectPosition:e.position},src:c.value.src,srcset:c.value.srcset,alt:e.alt,crossorigin:e.crossorigin,referrerpolicy:e.referrerpolicy,draggable:e.draggable,sizes:e.sizes,ref:v,onLoad:k,onError:p},null),x=(L=t.sources)==null?void 0:L.call(t);return u(te,{transition:e.transition,appear:!0},{default:()=>[me(x?u("picture",{class:"v-img__picture"},[x,h]):h,[[Ht,m.value==="loaded"]])]})},W=()=>u(te,{transition:e.transition},{default:()=>[c.value.lazySrc&&m.value!=="loaded"&&u("img",{class:["v-img__img","v-img__img--preload",P.value],style:{objectPosition:e.position},src:c.value.lazySrc,alt:e.alt,crossorigin:e.crossorigin,referrerpolicy:e.referrerpolicy,draggable:e.draggable},null)]}),j=()=>t.placeholder?u(te,{transition:e.transition,appear:!0},{default:()=>[(m.value==="loading"||m.value==="error"&&!t.error)&&u("div",{class:"v-img__placeholder"},[t.placeholder()])]}):null,I=()=>t.error?u(te,{transition:e.transition,appear:!0},{default:()=>[m.value==="error"&&u("div",{class:"v-img__error"},[t.error()])]}):null,R=()=>e.gradient?u("div",{class:"v-img__gradient",style:{backgroundImage:`linear-gradient(${e.gradient})`}},null):null,D=F(!1);{const h=A(S,x=>{x&&(requestAnimationFrame(()=>{requestAnimationFrame(()=>{D.value=!0})}),h())})}return N(()=>{const h=Re.filterProps(e);return me(u(Re,be({class:["v-img",{"v-img--booting":!D.value},i.value,r.value,e.class],style:[{width:w(e.width==="auto"?b.value:e.width)},s.value,e.style]},h,{aspectRatio:S.value,"aria-label":e.alt,role:e.alt?"img":void 0}),{additional:()=>u(Ae,null,[u(O,null,null),u(W,null,null),u(R,null,null),u(j,null,null),u(I,null,null)]),default:t.default}),[[Ge("intersect"),{handler:y,options:e.options},null,{once:!0}]])}),{currentSrc:o,image:v,state:m,naturalWidth:b,naturalHeight:d}}}),Vn=C({disabled:Boolean,group:Boolean,hideOnLeave:Boolean,leaveAbsolute:Boolean,mode:String,origin:String},"transition");function T(e,n,a){return V()({name:e,props:Vn({mode:a,origin:n}),setup(t,i){let{slots:s}=i;const r={onBeforeEnter(l){t.origin&&(l.style.transformOrigin=t.origin)},onLeave(l){if(t.leaveAbsolute){const{offsetTop:o,offsetLeft:v,offsetWidth:m,offsetHeight:b}=l;l._transitionInitialStyles={position:l.style.position,top:l.style.top,left:l.style.left,width:l.style.width,height:l.style.height},l.style.position="absolute",l.style.top=`${o}px`,l.style.left=`${v}px`,l.style.width=`${m}px`,l.style.height=`${b}px`}t.hideOnLeave&&l.style.setProperty("display","none","important")},onAfterLeave(l){if(t.leaveAbsolute&&(l!=null&&l._transitionInitialStyles)){const{position:o,top:v,left:m,width:b,height:d}=l._transitionInitialStyles;delete l._transitionInitialStyles,l.style.position=o||"",l.style.top=v||"",l.style.left=m||"",l.style.width=b||"",l.style.height=d||""}}};return()=>{const l=t.group?Wt:re;return ie(l,{name:t.disabled?"":e,css:!t.disabled,...t.group?void 0:{mode:t.mode},...t.disabled?{}:r},s.default)}}})}function yt(e,n){let a=arguments.length>2&&arguments[2]!==void 0?arguments[2]:"in-out";return V()({name:e,props:{mode:{type:String,default:a},disabled:Boolean},setup(t,i){let{slots:s}=i;return()=>ie(re,{name:t.disabled?"":e,css:!t.disabled,...t.disabled?{}:n},s.default)}})}function bt(){let e=arguments.length>0&&arguments[0]!==void 0?arguments[0]:"";const a=(arguments.length>1&&arguments[1]!==void 0?arguments[1]:!1)?"width":"height",t=ze(`offset-${a}`);return{onBeforeEnter(r){r._parent=r.parentNode,r._initialStyle={transition:r.style.transition,overflow:r.style.overflow,[a]:r.style[a]}},onEnter(r){const l=r._initialStyle;r.style.setProperty("transition","none","important"),r.style.overflow="hidden";const o=`${r[t]}px`;r.style[a]="0",r.offsetHeight,r.style.transition=l.transition,e&&r._parent&&r._parent.classList.add(e),requestAnimationFrame(()=>{r.style[a]=o})},onAfterEnter:s,onEnterCancelled:s,onLeave(r){r._initialStyle={transition:"",overflow:r.style.overflow,[a]:r.style[a]},r.style.overflow="hidden",r.style[a]=`${r[t]}px`,r.offsetHeight,requestAnimationFrame(()=>r.style[a]="0")},onAfterLeave:i,onLeaveCancelled:i};function i(r){e&&r._parent&&r._parent.classList.remove(e),s(r)}function s(r){const l=r._initialStyle[a];r.style.overflow=r._initialStyle.overflow,l!=null&&(r.style[a]=l),delete r._initialStyle}}T("fab-transition","center center","out-in");T("dialog-bottom-transition");T("dialog-top-transition");const Gn=T("fade-transition");T("scale-transition");T("scroll-x-transition");T("scroll-x-reverse-transition");T("scroll-y-transition");T("scroll-y-reverse-transition");T("slide-x-transition");T("slide-x-reverse-transition");const jn=T("slide-y-transition");T("slide-y-reverse-transition");const Un=yt("expand-transition",bt()),qn=yt("expand-x-transition",bt("",!0));export{hn as A,qe as B,qt as C,Ke as D,oe as E,we as F,Jt as G,gn as H,Ut as I,qn as J,Un as K,An as L,te as M,Mn as N,un as O,it as P,vn as Q,wn as R,cn as S,rt as T,fn as U,Fn as V,Hn as W,jn as X,En as Y,ce as a,Xe as b,Je as c,le as d,pe as e,Qe as f,Ye as g,ae as h,ge as i,ue as j,at as k,st as l,Ue as m,In as n,Rn as o,Ft as p,zn as q,Nn as r,On as s,Wn as t,Mt as u,Dn as v,Xt as w,Kt as x,Gn as y,Yt as z};
