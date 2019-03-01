# encoding: utf-8

"""
TODO:
    * OK dériver de windows et finir pour tous les types de base pour un seul objet
      et avec les Class HBDS
    * OK faire les att composés
    * OK contrôle des types après saisie
        pas de contôle de type par widget à la volée car il faut des widgets
        spécifique qui ne sont pas faciles à ajouter.
        Donc on fait ça en signalant les erreurs. Pour l'instant le message de l'exception
        est remonté.
    * OK les unités. Reste encore a faire que l'on puisse la changer
    * OK choix du positionnement vertical ou horizontal des att
    * OK ajouter plusieurs objets
    * OK disabled AttrElements
    * ajouter la modification en mode MVC des objets
    * faire les querytree
    * les traductions + locales
    * doc et tooltips
    * undo/redo
    * choix du positionnement des noms attrs:
       * à gauche, à droite des champs,
       * justifié à gauche ou à droite
            
"""
import pathlib
from ADT import basictypes, fonctors, hbds, units
import PySimpleGUI as sg
from ADT import images

CALENDAR_ICON = pathlib.Path(__file__, '../calendar.png')


def boolWidget(valtype, val, key, disabled=False, size=(None,None)):
    if val is None: val = False
    return [
        sg.Check('', default=val, key=key,
                 change_submits=True, disabled=disabled),
        ]

def red_greenButtons(valtype, val, key, disabled=False, size=(None,None)):
    if val is None:
        img = images.mac_gray
    else:
        img = images.mac_green if val else images.mac_red
    b = sg.Button('', image_data=img, key=key, #change_submits=True,
                  button_color=(sg.DEFAULT_BACKGROUND_COLOR, sg.COLOR_SYSTEM_DEFAULT),
                  border_width=0, disabled=disabled, target=key
                  )
    return [b]  

def intWidget(valtype, val, key, disabled=False, size=(None,None)):
    if val is None: val = ''
    return [
        sg.In(val, key=key, change_submits=True, do_not_clear=True,
              size=(20,1), disabled=disabled),
        ]

def floatWidget(valtype, val, key, disabled=False, size=(None,None)):
    if val is None: val = ''
    return [
        sg.In(val, key=key, change_submits=True, do_not_clear=True,
              size=(20,1), disabled=disabled),
        ]

def strWidget(valtype, val, key, disabled=False, size=(None,None)):
    if val is None: val = ''
    return [
        sg.In(val, key=key, change_submits=True, do_not_clear=True,
              size=(20,1), disabled=disabled),
        ]

def EnumWidget(valtype, val, key, disabled=False, size=(None,None)):
    V = [e.name for e in valtype] + ['None']
    # ajoute 2 à la longueur car si non la flêche de la combo cache la fin du text
    S = (max([len(v) for v in V])+2, sg.DEFAULT_ELEMENT_SIZE[1])
    return [
        sg.Combo(values=V, size=S,
                 default_value=val.name if val else 'None',
                 key=key, change_submits=True, disabled=disabled),
        ]

def dateWidget(valtype, val, key, disabled=False, size=(None,None)):
    if val is None: val = ''
    return [
        sg.In(val, size=(20,1), key=key, change_submits=True, do_not_clear=True,
              disabled=disabled),
        sg.CalendarButton("", target=key,
                          default_date_m_d_y=(val.month, val.day, val.year),
                          image_filename=CALENDAR_ICON,
                          image_size=(25, 25),
                          image_subsample=1,
                          border_width=0),
        ]

def timeWidget(valtype, val, key, disabled=False, size=(None,None)):
    if val is None: val = ''
    return [
        sg.In(val, size=(20,1), key=key, change_submits=True, do_not_clear=True,
              disabled=disabled),
        ]

def datetimeWidget(valtype, val, key, disabled=False, size=(None,None)):
    if val is None: val = ''
    return [
        sg.In(val, size=(20,1), key=key, change_submits=True, do_not_clear=True,
              disabled=disabled),
        sg.CalendarButton("", target=key,
                          default_date_m_d_y=(val.month, val.day, val.year),
                          image_filename=CALENDAR_ICON,
                          image_size=(30, 30),
                          image_subsample=1,
                          border_width=0),
        ]

def ColorWidget(valtype, val, key, disabled=False, size=(None,None)):
    if val is None: val = ''
    return [
        sg.In(val, size=(8,1), key=key, change_submits=True, do_not_clear=True,
              disabled=disabled),
        sg.ColorChooserButton('' if val else '?', key='__'+key, size=(2,1),
                              target=key, button_color=(val,val) if val else (None,None)),
        ]

def PathWidget(valtype, val, key, disabled=False, size=(None,None)):
    if val is None: val = basictypes.Path('.')
    if val.is_dir():
        return [
            sg.In(val, key=key, do_not_clear=True, change_submits=True,
                  disabled=disabled),
            sg.FolderBrowse(target=key, initial_folder=val, disabled=disabled)
            ]
    else:
        return [
            sg.In(val, key=key, do_not_clear=True, change_submits=True,
                  disabled=disabled),
            sg.FileBrowse(target=key, initial_folder=val, disabled=disabled)
            ]


type_to_widget = {
    bool:                   boolWidget, #red_greenButtons,
    int:                    intWidget,
    float:                  floatWidget,
    str:                    strWidget,
    basictypes.Enum:        EnumWidget,
    basictypes.date:        dateWidget,
    basictypes.time:        timeWidget,
    basictypes.datetime:    datetimeWidget,
    basictypes.Color:       ColorWidget,
    basictypes.Path:        PathWidget,
    }

def basicWidget(valtype, val, key, disabled=False, size=(None,None)):
    if valtype:
        widget = None
        for t in valtype.__mro__:
            wtype = type_to_widget.get(t, None)
            if wtype:
                widget = wtype(valtype, val, key, disabled=disabled, size=size)
            if widget:
                return widget
            
    return [sg.T("Unknown widget for %s" % valtype)]        

    
def make_keys(obj, attr):
    idobj = id(obj)
    attr_key = "%s.%s" %(idobj, attr)
    attrlabel_key = "_%s.%s" %(idobj, attr)
    return attrlabel_key, attr_key

def id_attr_from_keys(key):
    print(key)
    ID, attr = key.split('.')
    return int(ID), attr

def is_hbds(obj):
    return isinstance(type(obj), hbds.Class)

def is_ComposedAtt(obj, attr):
    typeattr = getattr(type(obj), attr)
    return type(typeattr).__name__.find('ComposedAtt_') != -1
            
def AttrElements(obj, attr, attrname_size=(None,None), attrinput_size=(None,None),
                 layout_type='align-left', disabled=False):
    layout = []
    val = getattr(obj, attr)
    nkey, key = make_keys(obj, attr)
    unit_widget = None
    if is_hbds(obj):
        if is_ComposedAtt(obj, attr):
            W = AttrsElements(val, None, attrname_size, attrinput_size,
                              layout_type, disabled)
            layout.append(sg.Frame(attr, W))
            return layout

        typeattr = getattr(type(obj), attr)
        valtype = typeattr.type
        
        if getattr(type(obj), attr).unit:
##            V = [v.symbol for v in list(type(typeattr.unit).__members__.values())]
##            print(V)
##            S = (max([len(v) for v in V]), sg.DEFAULT_ELEMENT_SIZE[1])
##            # bug dans PySimpleGUI ligne 5097: feild non unique!
##            unit_widget = sg.Combo(values=V, size=S,
##                                   default_value=typeattr.unit.name,
##                                   key="u_"+key, change_submits=True)
            # Ou juste le symbol
            unit_widget = sg.T(typeattr.unit.symbol, tooltip=typeattr.unit.name)
            
    else: # No hbds.Class
        valtype = type(val)

    layout = basicWidget(valtype, val, key, disabled=disabled)
    err_button = sg.Button("?", visible=False, key="?"+nkey)

    if   layout_type == 'align-left':
        label = sg.T(attr, size=attrname_size, key=nkey, pad=(0,0),
                     auto_size_text=False, justification='left')
        layout = [label] + layout + [err_button]
    elif layout_type == 'align-center-left':
        label = sg.T(attr, size=attrname_size, key=nkey, pad=(0,0),
                     auto_size_text=False, justification='right')
        layout = [label] + layout + [err_button]
    elif layout_type == 'align-right':
        label = sg.T(attr, size=attrname_size, key=nkey, pad=(0,0),
                     auto_size_text=False, justification='right')
        layout = layout + [label, err_button]
    elif layout_type == 'align-center-right':
        label = sg.T(attr, size=attrname_size, key=nkey, pad=(0,0),
                     auto_size_text=False, justification='left')
        layout = layout + [label, err_button]
    else:
        msg = "layout_type param must be in (align-left, "
        msg += "align-right, align-center-left, align-center-right). "
        msg += "Is '%s'." % layout_type
        raise ValueError(msg)
    
    if unit_widget:
        layout.append(unit_widget)

    return layout

def AttrsElements(obj, attrs=None, attrname_size=(None,None),
                 attrinput_size=(None,None), layout_type='align-left', disabled=False):
    if attrs is None:
        attrs = [a for a in fonctors.getattrs(obj)]
    attrname_size = (
        max([len(a) for a in attrs]),
        sg.DEFAULT_ELEMENT_SIZE[1]
        )
    print(attrname_size)

    layout = []
    for attr in attrs:
        W = AttrElements(obj, attr, attrname_size, attrinput_size, layout_type, disabled)
        layout.append(W)
    return layout

def convert_enum(pytype, val):
    if basictypes.Enum not in pytype.__mro__: return val
    if val == 'None':
        return None
    return getattr(pytype, val, val)
        
class ADTWindow(sg.Window):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.objects = {}
        self.errors = {}
        
    def Layout(self, objects, layout):
        self.objects.update(dict([(id(o), o) for o in objects]))
        return super().Layout(layout).Finalize()
        
    def Read(self, timeout=None, timeout_key=sg.TIMEOUT_KEY):
        event, values = super().Read(timeout, timeout_key)
        if event is None: return event, values

        if event[0:2] == "?_":
            sg.PopupError(self.errors[event[2:]])
            return event, values

        try:
            i, attr = id_attr_from_keys(event)
        except ValueError:
            return event, values
        
        try:
            obj = self.objects[i]
        except KeyError:
            return event, values

        try:
            newval = values[event]
        except KeyError: # if widget is not input widget as defined by PySimpleGui
            return event, values
        
        if newval == '': newval = None
        
        # try to validate new value
        try:
            if is_hbds(obj):
                pytype = getattr(type(obj), attr).type
                newval = convert_enum(pytype, newval)
                print(newval)
                newval = getattr(type(obj), attr)._validate(newval)
            else:
                pytype = type(getattr(obj, attr))
                newval = convert_enum(pytype, newval)
                newval = pytype(newval)
        except (TypeError, ValueError) as e:
            self.FindElement('_'+event).Update(text_color='red')
            self.FindElement('?_'+event).Update(visible=True)
            #self.FindElement(event).Update(getattr(obj, attr))
            self.errors[event] = str(e)
            return event, values

        # update helper basetype button
        if isinstance(newval, basictypes.Color):
            self.FindElement('__'+event).Update(text='', button_color=(None,newval))

        # reset label and help if no errors
        self.FindElement('_'+event).Update(text_color=sg.DEFAULT_TEXT_COLOR)
        self.FindElement('?_'+event).Update(visible=False)
        if event in self.errors:
            del self.errors[event]

        return event, values

def show_py_object():
    class X: pass
    Genre = basictypes.Enum('Genre', "Homme Femme XXY YYX XYX")

    x = X()
    x.nom = "xx"
    x.age = 12
    x.taille = 1.8
    x.marie = True
    x.date_de_naissance = basictypes.date("19/08/1963")
    x.heure_de_naissance = basictypes.time(10)
    x.genre = Genre.Homme
    x.X = []
    x.now = basictypes.datetime.now()
        
    window = ADTWindow('py object', resizable=True).Layout( (x,), AttrsElements(x))

    while True:
      event, values = window.Read()
      if event is None: return
      print(event, values)

def show_hbds_object():

    Blindage = basictypes.Enum('Blindage', "dur mou")

    class Equipement(metaclass=hbds.Class):
        nom = str, "toto"
        blindage = Blindage
        volume = float, units.CubicMeter.cubic_meter
        masse = float, units.Kilogram.tonne
        filtration_d_air = bool
        dimensions = hbds.ComposedAtt(
            longueur = (float, units.Meter.metre),
            largeur = (float, units.Meter.metre),
            )
        pente = hbds.ComposedAtt(
            pente_max = float, # degré
            ralentissement = float, # pourcent
            )
        color = basictypes.Color

    e1 = Equipement(nom="1")
    e2 = Equipement(nom="2", blindage=Blindage.dur)
    W = AttrsElements(e1, layout_type='align-center-left')
    W1 = AttrsElements(e2, ["nom", "blindage", "volume", "masse", "filtration_d_air"] )
    W2 = AttrsElements(e2, ["dimensions", "pente"] )

    O = (e1, e2, e1.dimensions, e1.pente, e2.dimensions, e2.pente)
    
    window = ADTWindow('ADT: Equipement').Layout( O,
                    [[sg.Column(W), sg.VSep(), sg.Column(W1), sg.VSep(), sg.Column(W2)]])

    while True:
      event, values = window.Read()
##      print(event, values)
      if event is None: return
      id, attr = id_attr_from_keys(event)
      obj = window.objects[id]
      nv = values[event]
      print("Changed: obj %s, attr %s, old value %s, new value %s" % \
            (obj, attr, nv, str(getattr(obj, attr))) )

def test_size():
    ST = (15,1)
    SI = (10,1)
    window = sg.Window('Test').Layout([
        [sg.T('A', size=ST), sg.In(size=SI)],
        [sg.T('A'*4, size=ST), sg.In(size=SI)],
        [sg.T('w'*15, size=ST), sg.In(size=SI)],
        ])

    while True:
      event, values = window.Read()
      if event is None: return
    
def main():
    import random
    # PB avec COLOR_SYSTEM_DEFAULT qui apparait trop souvent
    index = random.choice(sg.ListOfLookAndFeelValues())
    colors = sg.LOOK_AND_FEEL_TABLE[index]
##    print(index, colors)

    sg.ChangeLookAndFeel(index)
    sg.DEFAULT_TEXT_COLOR = colors['TEXT']
    sg.SetOptions(
        font=('Times', 12),
        auto_size_text=True
        )
##    print(sg.DEFAULT_TEXT_COLOR)

    #show_py_object()
    show_hbds_object()
    #test_size()
    
if __name__ == '__main__':
    main()

