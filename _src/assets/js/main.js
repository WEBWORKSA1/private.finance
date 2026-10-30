/* Private.Finance — core site script (no trackers, no frameworks) */
(function(){
  "use strict";
  var PF = window.PF = window.PF || {};
  PF.config = {
    adClient: "ca-pub-6620975821265271",
    /* Paste AdSense ad-unit slot IDs here once created in AdSense → Ads → By ad unit.
       Until then, Auto ads (enabled in the AdSense dashboard) place ads automatically. */
    adSlots: { top: "", inArticle: "", sidebar: "", footer: "" },
    /* Optional: once FormSubmit sends its activation email, you can replace the inbox
       route with the random alias it gives you (e.g. "a1b2c3d4e5..."). */
    formAlias: ""
  };

  /* ---------- storage helpers (never throw) ---------- */
  PF.store = {
    get:function(k,d){try{var v=localStorage.getItem("pf_"+k);return v===null?d:JSON.parse(v);}catch(e){return d;}},
    set:function(k,v){try{localStorage.setItem("pf_"+k,JSON.stringify(v));}catch(e){}}
  };

  /* ---------- protected inbox (never rendered as text) ---------- */
  var _k=["__E1__","__E2__"];
  function inbox(){try{return atob(_k[0]).split("").reverse().join("")+String.fromCharCode(64)+atob(_k[1]);}catch(e){return "";}}
  PF.mailto=function(subject,body){
    var u="mai"+"lto:"+inbox()+"?subject="+encodeURIComponent(subject||"Private.Finance inquiry");
    if(body)u+="&body="+encodeURIComponent(body);
    window.location.href=u;
  };
  PF.donate=function(amount,purpose,currency,monthly){
    var u="https://www.paypal.com/donate/?business="+encodeURIComponent(inbox())+"&no_recurring="+(monthly?"0":"1")+
      "&item_name="+encodeURIComponent("Support Private.Finance — "+(purpose||"General operations"))+
      "&currency_code="+encodeURIComponent(currency||"USD");
    if(amount>0)u+="&amount="+encodeURIComponent(amount);
    window.open(u,"_blank","noopener");
  };
  document.addEventListener("click",function(e){
    var a=e.target.closest("[data-mail]");
    if(a){e.preventDefault();PF.mailto(a.getAttribute("data-mail")||"Private.Finance inquiry");}
  });

  /* ---------- theme ---------- */
  var root=document.documentElement;
  var saved=PF.store.get("theme",null);
  if(saved)root.setAttribute("data-theme",saved);
  document.addEventListener("click",function(e){
    if(e.target.closest("[data-theme-toggle]")){
      var t=root.getAttribute("data-theme")==="dark"?"light":"dark";
      root.setAttribute("data-theme",t);PF.store.set("theme",t);
    }
  });

  /* ---------- mobile nav ---------- */
  var burger=document.querySelector(".burger"),menu=document.querySelector(".menu");
  if(burger&&menu){burger.addEventListener("click",function(){var o=menu.classList.toggle("open");burger.setAttribute("aria-expanded",o);});}

  /* ---------- cookie notice ---------- */
  var ck=document.querySelector(".cookie");
  if(ck&&!PF.store.get("cookie_ok",false)){ck.classList.add("show");}
  document.addEventListener("click",function(e){
    var b=e.target.closest("[data-cookie]");
    if(b){PF.store.set("cookie_ok",b.getAttribute("data-cookie"));ck&&ck.classList.remove("show");}
  });

  /* ---------- reveal on scroll ---------- */
  if("IntersectionObserver" in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){en.target.classList.add("in");io.unobserve(en.target);}});},{rootMargin:"0px 0px -60px"});
    document.querySelectorAll(".reveal").forEach(function(el){io.observe(el);});
  } else document.querySelectorAll(".reveal").forEach(function(el){el.classList.add("in");});

  /* ---------- ad slots (manual units, optional) ---------- */
  document.querySelectorAll("[data-ad]").forEach(function(box){
    var slot=PF.config.adSlots[box.getAttribute("data-ad")];
    if(!slot)return;
    box.innerHTML='<div class="ad-label">Advertisement</div><ins class="adsbygoogle" style="display:block" data-ad-client="'+PF.config.adClient+'" data-ad-slot="'+slot+'" data-ad-format="auto" data-full-width-responsive="true"></ins>';
    try{(window.adsbygoogle=window.adsbygoogle||[]).push({});}catch(e){}
  });

  /* ---------- YouTube click-to-load (privacy-enhanced) ---------- */
  document.addEventListener("click",function(e){
    var v=e.target.closest(".vid[data-id]");
    if(!v||v.querySelector("iframe"))return;
    var id=v.getAttribute("data-id");
    v.innerHTML='<iframe src="https://www.youtube-nocookie.com/embed/'+id+'?autoplay=1&rel=0" title="'+(v.getAttribute("data-title")||"Video")+'" allow="accelerometer;autoplay;clipboard-write;encrypted-media;gyroscope;picture-in-picture" allowfullscreen loading="lazy"></iframe>';
  });

  /* ---------- forms → protected inbox via FormSubmit ---------- */
  function endpoint(){return "https://formsubmit.co/ajax/"+(PF.config.formAlias||inbox());}
  function serialize(form){
    var data={};
    new FormData(form).forEach(function(v,k){
      if(k==="_honey")return;
      data[k]=data[k]?data[k]+", "+v:v;
    });
    return data;
  }
  PF.submit=function(form,extra){
    var msg=form.querySelector(".form-msg");
    if(!msg){msg=document.createElement("div");msg.className="form-msg";form.appendChild(msg);}
    var hp=form.querySelector("[name=_honey]");
    if(hp&&hp.value){return Promise.resolve(false);}
    var data=serialize(form);
    if(extra)for(var k in extra)data[k]=extra[k];
    data._subject=(data._subject||form.getAttribute("data-subject")||"Website form")+" — Private.Finance";
    data._template="table";
    data._captcha="false";
    data.page=location.href;
    data.submitted=new Date().toISOString();
    var btn=form.querySelector("[type=submit]");
    if(btn){btn.disabled=true;btn.dataset.t=btn.textContent;btn.textContent="Sending…";}
    msg.className="form-msg";msg.textContent="";
    return fetch(endpoint(),{method:"POST",headers:{"Content-Type":"application/json","Accept":"application/json"},body:JSON.stringify(data)})
      .then(function(r){return r.json().catch(function(){return {};}).then(function(j){if(!r.ok||j.success==="false"||j.success===false)throw new Error(j.message||"send failed");return j;});})
      .then(function(){
        msg.className="form-msg ok";
        msg.textContent=form.getAttribute("data-ok")||"Thank you — your message has been received. We reply within 1–2 business days.";
        form.reset();
        form.dispatchEvent(new CustomEvent("pf:sent"));
        return true;
      })
      .catch(function(){
        msg.className="form-msg err";
        msg.innerHTML='We couldn\'t send that automatically. <a href="#" data-mail="'+(data._subject||"Inquiry")+'">Click here to send it by email instead</a>.';
        var lines=[];for(var k in data){if(k.charAt(0)!=="_")lines.push(k+": "+data[k]);}
        PF._fallbackBody=lines.join("\n");
        return false;
      })
      .finally(function(){if(btn){btn.disabled=false;btn.textContent=btn.dataset.t;}});
  };
  document.addEventListener("click",function(e){
    var a=e.target.closest(".form-msg [data-mail]");
    if(a&&PF._fallbackBody){e.preventDefault();e.stopPropagation();PF.mailto(a.getAttribute("data-mail"),PF._fallbackBody);}
  },true);
  document.querySelectorAll("form[data-pf]").forEach(function(f){
    f.addEventListener("submit",function(e){e.preventDefault();if(!f.reportValidity||f.reportValidity())PF.submit(f);});
  });

  /* ---------- currency ---------- */
  var CUR={USD:"en-US",CAD:"en-CA",GBP:"en-GB",EUR:"de-DE",INR:"en-IN",AUD:"en-AU",LKR:"en-LK",AED:"en-AE"};
  PF.currency=PF.store.get("currency","USD");
  PF.fmt=function(n,dec){
    if(!isFinite(n))return "—";
    try{return new Intl.NumberFormat(CUR[PF.currency]||"en-US",{style:"currency",currency:PF.currency,maximumFractionDigits:dec||0,minimumFractionDigits:dec||0}).format(n);}
    catch(e){return PF.currency+" "+Math.round(n).toLocaleString();}
  };
  PF.sym=function(){try{return (0).toLocaleString(CUR[PF.currency],{style:"currency",currency:PF.currency,maximumFractionDigits:0}).replace(/[\d\s.,]/g,"");}catch(e){return "$";}};
  function paintSym(){document.querySelectorAll(".pre[data-cur]").forEach(function(s){s.textContent=PF.sym();});}
  document.querySelectorAll("select[data-currency]").forEach(function(s){
    s.value=PF.currency;
    s.addEventListener("change",function(){PF.currency=s.value;PF.store.set("currency",s.value);paintSym();document.dispatchEvent(new Event("pf:currency"));});
  });
  paintSym();

  /* ---------- table of contents ---------- */
  var toc=document.querySelector(".toc[data-auto]");
  if(toc){
    var hs=document.querySelectorAll(".prose h2[id]");
    hs.forEach(function(h){var a=document.createElement("a");a.href="#"+h.id;a.textContent=h.textContent;toc.appendChild(a);});
    if("IntersectionObserver" in window){
      var tio=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){toc.querySelectorAll("a").forEach(function(a){a.classList.toggle("active",a.getAttribute("href")==="#"+en.target.id);});}});},{rootMargin:"0px 0px -70% 0px"});
      hs.forEach(function(h){tio.observe(h);});
    }
  }

  /* ---------- site search ---------- */
  var modal=document.querySelector(".search-modal"),idx=null;
  function openSearch(){
    if(!modal)return;modal.classList.add("open");var inp=modal.querySelector("input");inp.value="";inp.focus();render("");
    if(!idx){fetch(PF.base+"search-index.json").then(function(r){return r.json();}).then(function(j){idx=j;render(inp.value);}).catch(function(){});}
  }
  function render(q){
    var box=modal.querySelector(".search-results");if(!idx){box.innerHTML='<p class="muted">Loading…</p>';return;}
    q=q.trim().toLowerCase();
    var hits=idx.filter(function(i){return !q||(i.t+" "+i.d+" "+i.k).toLowerCase().indexOf(q)>-1;}).slice(0,12);
    box.innerHTML=hits.length?hits.map(function(h){return '<a href="'+PF.base+h.u+'"><b>'+h.t+'</b><small>'+h.c+' · '+h.d+'</small></a>';}).join(""):'<p class="muted">No matches. Try “budget”, “mortgage” or “advisor”.</p>';
  }
  document.addEventListener("click",function(e){
    if(e.target.closest("[data-search]")){e.preventDefault();openSearch();}
    if(modal&&e.target===modal)modal.classList.remove("open");
  });
  document.addEventListener("keydown",function(e){
    if((e.key==="/"&&!/input|textarea|select/i.test(document.activeElement.tagName))||((e.metaKey||e.ctrlKey)&&e.key==="k")){e.preventDefault();openSearch();}
    if(e.key==="Escape"&&modal)modal.classList.remove("open");
  });
  if(modal)modal.querySelector("input").addEventListener("input",function(e){render(e.target.value);});

  /* ---------- year ---------- */
  document.querySelectorAll("[data-year]").forEach(function(s){s.textContent=new Date().getFullYear();});
})();
