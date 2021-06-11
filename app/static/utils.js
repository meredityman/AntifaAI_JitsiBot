String.prototype.hashCode = function() {
  var hash = 0;
  if (this.length == 0) {
      return hash;
  }
  for (var i = 0; i < this.length; i++) {
      var char = this.charCodeAt(i);
      hash = ((hash<<5)-hash)+char;
      hash = hash & hash; // Convert to 32bit integer
  }
  return hash;
}

class MeetingDetails{
  constructor(element, meetingUrl){
    this.element      = element;
    this.uptime = null;

    this.element.find("#meeting-link").attr("href", meetingUrl)

  }
}



class EventSelector{

  constructor(element, sendPublicMessageCallback){
    this.element      = element;
    for (const [name, value] of Object.entries(messageEvents)) {
      console.info(name, value);
      var button = $('<button/>', {
          text: name, 
          id: 'btn_'+ name.replace(/ /g,"_"),
          click: function () { 
            if(value['target'] == 'all'){
              console.info(value['message']);
              sendPublicMessageCallback(value['message']);
            }
          }
      });
      this.element.append(button);
    }
  }
};

class InteractionSelector{
  constructor(element, interactionList, setInteractionEngine){
    this.element      = element;
    this.setInteractionEngine = setInteractionEngine;

    let buttons = [];

    interactionList.forEach( (interactionName) => {

      var button = $('<button/>', {
        text: interactionName, 
        id: 'btn-' + interactionName,
        click: function () { 
          setInteractionEngine(interactionName);

          buttons.forEach( item => {

            if(item.attr('id') == $(this).attr('id') ){
              item.addClass('selected');
            } else {
              item.removeClass('selected');
            }
          })
        }
      });

      buttons.push(button);
      this.element.append(button);
    });  

  }

  
};

class MessageList {
  constructor(element, ownUid, displayName){
    this.element      = element;
    this.ownUid = ownUid;
    this.displayName = displayName;
    this.publicMessages = [];
    this.privateMessages = {};


    this.publicMessageElement  = $(`<div id="public-messages"></div>`).appendTo(element);
    this.privateMessageElement = $(`<div id="private-messages"></div>`).appendTo(element);
  };

  addPublicMessage(uid, displayName, message){

    this.publicMessages.push({
      'uid'  : uid,
      'text' : message
    });

    this.publicMessageElement.append(`<p class="message">${displayName} - ${message}</p>`);
  };

  addPrivateMessage(uid, displayName, message){
    if(!(uid in this.privateMessages)){
      this.privateMessages[uid] = [];
    }

    this.privateMessages[uid].push( {
      'uid'  : uid,
      'text' : message
    });

    let messageEl = $('#private-messages-' + uid);
    if(!messageEl.length){
      messageEl = $(`<div id="${'#private-messages-' + uid}"></div>`).appendTo(this.privateMessageElement);
    }
    messageEl.append(`<p class="message">${displayName} - ${message}</p>`);

  }

  addPrivateReply(uid, message){
    if(!(uid in this.privateMessages)){
      this.privateMessages[uid] = [];
    }

    this.privateMessages[uid].push( {
      'uid'  : this.ownUid,
      'text' : message
    });

    let messageEl = $('#private-messages-' + uid);
    if(!messageEl.length){
      messageEl = $(`<div id="${'#private-messages-' + uid}"></div>`).appendTo(this.privateMessageElement);
    }
    messageEl.append(`<p class="message">${this.displayName} - ${message}</p>`);

  }

};

class UserList {
  constructor(element, participants, selectionChangedCallback) {
      this.element      = element
      this.selectionChangedCallback = selectionChangedCallback;
      this.selectedUids = new Set();


      // this.participants = Object.assign({}, ...participants.map((x) => ({[x._id]: x})));
      this.participants = {};
      this.listEl = $('<ul id="element-list-ul"></ul>');
      this.element.append(this.listEl);
      Object.values(participants).forEach(user => {
        this.addUser(user);
      });

  };

  getSelectedIds(){
    return Array.from(this.selectedUids);
  }

  getDisplayName(uid){
    if( uid in this.participants){
      return this.participants._displayName;
    } else {
      return "Unknown"
    }
  }

  addButton(element, selected){
    let uid = element._id
    let text = element._displayName + " (" + uid + ")";
    let id = 'element-btn-' + uid;

    let userList = this;

    function callback(){
      userList.participants[uid]['selected'] = !userList.participants[uid]['selected']
      $( this ).toggleClass( "selected" );

      if(userList.participants[uid]['selected']){
        userList.selectedUids.add(uid);
      } else {
        userList.selectedUids.delete(uid);
      }
      userList.selectionChangedCallback(userList.getSelectedIds());
    }

    let button = $('<button/>', {
        text: text, 
        id: id,
        class : 'element-btn',
        click: callback
    });

    if (selected){
      button.addClass('selected');
      userList.selectedUids.add(uid);
    }

    return button;
  }

  addUser( user, selected = true){
    console.log("Adding element " + user._id);
    user['selected'] = selected;
    this.participants[user._id] = user;

    let button = this.addButton(user, selected);
    button = button.wrap('<li class="list-group-item"></li>').parent();
    this.listEl.append(button);
  };

  removeUser( user){
    console.log("Removing element " + user._id);
    delete this.participants[user._id];
    this.listEl.find('#element-btn-' + user._id).parent().remove();

    if(this.selectedUids.delete(user._id)){
      this.selectionChangedCallback(this.selectedUids);
    };
  };

  getDisplayName(uid){
    if( uid in this.participants){
      return this.participants[uid]._displayName;  
    } else {
      return null
    }
  }

};