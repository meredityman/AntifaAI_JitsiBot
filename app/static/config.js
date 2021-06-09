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
