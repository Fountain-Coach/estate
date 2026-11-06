/* Fountain Press: source-faithful Teatro instrument citation within the existing reader.
 * The original instruments are immutable Teatro Git snapshots, not new synths.
 * This creates an on-demand full-bleed performance sheet, never an iframe
 * inside the Linotype page measurement tree. Closing restores the same folio.
 */
const citationSources=Object.freeze({
 v156:{title:'Kino After Dark · original groove synthesizer',
       source:'Teatro f3f7d39 · AAC-compatible source 35fd6a4',
       href:'/teatro/interludes/kino/press-citation/v156/'},
 v158:{title:'Kino After Dark · original cinematic synthesizer',
       source:'Teatro edd6929 · complete source e2f5dd2',
       href:'/teatro/interludes/kino/press-citation/v158/'}
});
let sheet=null,previousFocus=null,sourceReadyTimer=null;
const styles=document.createElement('style');
styles.textContent=`
.press-source-sheet{position:fixed;inset:0;width:100vw;height:100dvh;max-width:none;max-height:none;margin:0;padding:0;border:0;background:#080b0d;color:#e3e8dd;overflow:hidden}
.press-source-sheet::backdrop{background:#080b0d}
.press-source-sheet-inner{display:grid;grid-template-rows:minmax(48px,auto) minmax(0,1fr);height:100%}
.press-source-top{display:flex;align-items:center;justify-content:space-between;gap:1rem;padding:.4rem clamp(12px,3vw,32px);border-bottom:1px solid #435e4f;background:#111b17}
.press-source-identity{min-width:0}
.press-source-identity strong{display:block;font:normal clamp(15px,2vw,20px) Georgia,serif}
.press-source-identity small{display:block;color:#a2b8a8;font:11px system-ui,sans-serif}
.press-source-close{border:1px solid #93b29c;border-radius:3px;background:transparent;color:#e6eee5;cursor:pointer;min-height:44px;min-width:90px;font:13px system-ui,sans-serif}
.press-source-close:focus-visible{outline:3px solid #a2e4c3;outline-offset:2px}
.press-source-original{display:block;width:100%;height:100%;border:0;background:#080b0d}
@media(max-width:560px){.press-source-identity small{font-size:9px}.press-source-top{gap:.45rem;padding:.3rem .6rem}.press-source-close{min-width:76px}}
`;
document.head.append(styles);
function closeCitation(){
 if(sourceReadyTimer){clearInterval(sourceReadyTimer);sourceReadyTimer=null}
 if(!sheet)return;
 const done=sheet;sheet=null;
 const frame=done.querySelector('iframe');
 if(frame){frame.src='about:blank';frame.remove()}
 if(done.open)done.close();
 done.remove();
 if(previousFocus?.isConnected)previousFocus.focus({preventScroll:true});
 previousFocus=null;
}
function openCitation(kind,button){
 const source=citationSources[kind];
 if(!source)return;
 closeCitation();
 previousFocus=button;
 const dialog=document.createElement('dialog');
 dialog.className='press-source-sheet';
 dialog.setAttribute('aria-label',source.title);
 dialog.innerHTML='<div class="press-source-sheet-inner"><div class="press-source-top">'+
   '<div class="press-source-identity"><strong></strong><small></small></div>'+
   '<button class="press-source-close" type="button" aria-label="Close original Kino instrument and return to reading">Close · Return</button>'+
   '</div></div>';
 dialog.querySelector('strong').textContent=source.title;
 const readiness=dialog.querySelector('small');
 readiness.setAttribute('aria-live','polite');
 readiness.textContent=source.source+' · Loading original source…';
 const frame=document.createElement('iframe');
 frame.className='press-source-original';
 frame.title=source.title+' · unmodified original Teatro source';
 frame.style.pointerEvents='none';
 frame.setAttribute('allow','autoplay');
 frame.setAttribute('sandbox','allow-scripts allow-same-origin');
 dialog.querySelector('.press-source-sheet-inner').append(frame);
 dialog.querySelector('.press-source-close').addEventListener('click',closeCitation);
 dialog.addEventListener('cancel',event=>{event.preventDefault();closeCitation()});
 dialog.addEventListener('close',closeCitation);
 document.body.append(dialog);
 sheet=dialog;
 dialog.showModal();
 frame.src=source.href;
 // An original Teatro module can arrive after its controls appear in the DOM.
 // Detect the source's own dynamically constructed sixteen windows; no changes
 // to its byte-identical script or interface and no invented timer-based readiness.
 const marker=kind==='v156'?'#kino-windows .window-step':'#kino-windows .memory-window';
 const begin=Date.now();
 sourceReadyTimer=setInterval(()=>{
   if(sheet!==dialog){clearInterval(sourceReadyTimer);sourceReadyTimer=null;return}
   try{
     if(frame.contentDocument?.querySelectorAll(marker).length===16){
       clearInterval(sourceReadyTimer);sourceReadyTimer=null;
       frame.style.pointerEvents='auto';
       readiness.textContent=source.source+' · Source ready · Play on the original instrument';
     }else if(Date.now()-begin>25000){
       clearInterval(sourceReadyTimer);sourceReadyTimer=null;
       readiness.textContent=source.source+' · Source could not initialize · Close and retry';
     }
   }catch{
     clearInterval(sourceReadyTimer);sourceReadyTimer=null;
     readiness.textContent=source.source+' · Source unavailable · Close and retry';
   }
 },70);
 dialog.querySelector('.press-source-close').focus();
}
document.addEventListener('click',event=>{
 const button=event.target.closest?.('[data-press-verbatim]');
 if(!button)return;
 const id=button.getAttribute('data-press-verbatim');
 if(!(id in citationSources))return;
 event.preventDefault();
 openCitation(id,button);
});
window.addEventListener('pagehide',closeCitation);
