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

function showTime(){
  var date = new Date();
  var h = date.getHours(); // 0 - 23
  var m = date.getMinutes(); // 0 - 59
  var s = date.getSeconds(); // 0 - 59
  var session = "AM";

  if(h == 0){
      h = 12;
  }

  if(h > 12){
      h = h - 12;
      session = "PM";
  }

  h = (h < 10) ? "0" + h : h;
  m = (m < 10) ? "0" + m : m;
  s = (s < 10) ? "0" + s : s;

  var time = h + ":" + m + ":" + s + " " + session;
  document.getElementById("MyClockDisplay").innerText = time;
  document.getElementById("MyClockDisplay").textContent = time;

  setTimeout(showTime, 1000);

}

class MeetingDetails{
  constructor(element, meetingUrl){
    this.element      = element;
    this.uptime = null;

    this.element.find("#meeting-link").attr("href", meetingUrl)

  }

}

class AvatarDetails{
  constructor(element){
    this.element      = element;
    this.uptime = null;

    let clock = $('<div id="MyClockDisplay" class="clock"></div>').appendTo(this.element);
    showTime();
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
  constructor(element, interactionList, sendEngineCommand, setInteractionEngine, engineConfig){
    this.element      = element;
    this.element.empty();
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

      if (interactionName == engineConfig["type"]){
        button.addClass('selected');  
      }

      buttons.push(button);
      this.element.append(button);
    });

    this.element.append($('<br/>'));

    let commands = engineConfig["commands"];

    if (commands) {
      commands.forEach( (command) => {

        var cbutton = $('<button/>', {
          text: command, 
          id: 'btn-' + engineConfig['type'] + '-' + command,
          click: function () { 
            sendEngineCommand(command);        }
        });
        this.element.append(cbutton);
      });  
    }
  }

  
};

class MessageList {
  constructor(element_public, element_private, ownUid, displayName){
    this.element_public      = element_public;
    this.element_private     = element_private;
    this.ownUid = ownUid;
    this.displayName = displayName;
    this.publicMessages = [];
    this.privateMessages = {};


    this.publicMessageElement  = $(`<div id="public-messages", class="message-list"</div>`).appendTo(element_public);
    this.privateMessageElement = $(`<div id="private-messages"></div>`).appendTo(element_private);
  };

  addPublicMessage(uid, displayName, message){
    if (message) {
      message = message.replace(/\n/g, "<br />");
      this.publicMessages.push({
        'uid'  : uid,
        'text' : message
      });
  
      this.publicMessageElement.append(`<p class="message"><span class="user-name">${displayName}</span> - ${message}</p>`);
      
      this.publicMessageElement.scrollTop(this.publicMessageElement[0].scrollHeight);
    }
  };

  addPrivateMessage(uid, displayName, message){
    if (message) {
      message = message.replace(/\n/g, "<br />");
      
      if(!(uid in this.privateMessages)){
        this.privateMessages[uid] = [];
      }

      this.privateMessages[uid].push( {
        'uid'  : uid,
        'text' : message
      });

      let messageEl = $('#private-messages-' + uid);
      console.warn(messageEl);
      if(!messageEl.length){
        messageEl = $(`<div id="${'private-messages-' + uid}", class="message-list"></div>`).appendTo(this.privateMessageElement);
      }
      messageEl.append(`<p class="message"><span class="user-name">${displayName}</span> - ${message}</p>`);
      messageEl.scrollTop(messageEl[0].scrollHeight);
    }
  };

  addPrivateReply(uid, message){
    this.addPrivateMessage(uid, "Me", message)
  }

};

class UserList {
  constructor(element, participants, selectionChangedCallback, selectable=true) {
      this.element      = element
      this.selectionChangedCallback = selectionChangedCallback;
      this.selectedUids = new Set();
      this.selectable = selectable;

      // this.participants = Object.assign({}, ...participants.map((x) => ({[x._id]: x})));
      this.participants = {};
      this.listEl = $('<ul id="user-list-ul"></ul>');
      this.element.append(this.listEl);
      Object.values(participants).forEach(user => {
        this.addUser(user, false);
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
    let htmlid = 'element-btn-' + uid;

    let userList = this;

    function callback(){
      userList.participants[uid]['selected'] = !userList.participants[uid]['selected']
      if(userList.participants[uid]['selected']){
        $(this).addClass('selected');
        userList.selectedUids.add(uid);
      }else{
        $(this).removeClass('selected');
        userList.selectedUids.delete(uid);
      };

      userList.selectionChangedCallback(userList.getSelectedIds());
    }

    let button = $('<button/>', {
        id   : htmlid,
        text: text, 
        name: uid,
        class : 'user-btn',
    });

    if( selected){
      button.addClass('selected')
    }

    if(this.selectable){
      button.click(callback);
    }

    return button;
  }

  setSelectedIds(uids){
    self.selectedUids = uids;

    this.listEl.find("button").each( (i, button) => {
      if( $(button).attr("name") in uids){
        $(button).addClass('selected');
      } else {
        $(button).removeClass('selected');
      }

    });
  
  }

  addUser( user, selected = false){
    console.log("Adding element " + user._id);
    user['selected'] = selected;
    this.participants[user._id] = user;

    if(selected){
      this.selectedUids.add(user._id);
    }

    let button = this.addButton(user, selected);
    button = button.wrap('<li class="list-group-item"></li>').parent();
    this.listEl.append(button);
  };

  updateUserName(uid, name){
    if(uid in this.participants){
      console.log("Updating user " + uid);
      this.participants[uid]._displayName = name;

      let text = name + " (" + uid + ")";
      this.listEl.find('#element-btn-' + uid).html(text)
    } else {
      console.warn(uid + " not in list.")
    }
   
  };
  

  removeUser( user){
    console.log("Removing element " + user._id);
    delete this.participants[user._id];
    this.listEl.find('#element-btn-' + user._id).parent().remove();

    if(this.selectedUids.delete(user._id)){
      console.warn(this.selectedUids);
      this.selectionChangedCallback(Array.from(this.selectedUids));
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