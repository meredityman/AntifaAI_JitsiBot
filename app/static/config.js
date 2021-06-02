// const config = {
//    hosts: {
//       domain: 'meet.beta.meet.jit.si',
//       muc: 'conference.meet.beta.meet.jit.si', 
//       focus: 'focus.meet.beta.meet.jit.si',
//    },
//    enableP2P: true, 
//    p2p: { 
//       enabled: true, 
//       preferH264: true, 
//       disableH264: true, 
//       useStunTurn: true,
//    }, 
//    useStunTurn: true, 
//    externalConnectUrl: 'https://meet.beta.meet.jit.si/http-pre-bind', 

//    bosh: '//meet.beta.meet.jit.si/http-bind', // FIXME: use xep-0156 for that

//    // The name of client node advertised in XEP-0115 'c' stanza
//    clientNode: 'meet.beta.meet.jit.si'
// }

const config = {
   hosts: {
      domain: 'meet.cobratheatercobra.com',
      muc   : 'conference.meet.cobratheatercobra.com', 
      focus : 'focus.meet.cobratheatercobra.com',
   }, 
   enableP2P: true, 
   p2p: { 
      enabled: true, 
      preferH264: true, 
      disableH264: true, 
      useStunTurn: true,
   }, 
   useStunTurn: true, 
   openBridgeChannel: true,
   bosh: 'https://meet.cobratheatercobra.com/http-bind', 
   websocket: 'wss://meet.cobratheatercobra.com/xmpp-websocket', 
   clientNode: 'http://jitsi.org/jitsimeet', 
  }
