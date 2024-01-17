function varargout = lancamento(varargin)
%LANCAMENTO MATLAB code file for lancamento.fig
%      LANCAMENTO, by itself, creates a new LANCAMENTO or raises the existing
%      singleton*.
%
%      H = LANCAMENTO returns the handle to a new LANCAMENTO or the handle to
%      the existing singleton*.
%
%      LANCAMENTO('Property','Value',...) creates a new LANCAMENTO using the
%      given property value pairs. Unrecognized properties are passed via
%      varargin to lancamento_OpeningFcn.  This calling syntax produces a
%      warning when there is an existing singleton*.
%
%      LANCAMENTO('CALLBACK') and LANCAMENTO('CALLBACK',hObject,...) call the
%      local function named CALLBACK in LANCAMENTO.M with the given input
%      arguments.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help lancamento

% Last Modified by GUIDE v2.5 08-Oct-2022 15:22:13

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @lancamento_OpeningFcn, ...
                   'gui_OutputFcn',  @lancamento_OutputFcn, ...
                   'gui_LayoutFcn',  [], ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
   gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before lancamento is made visible.
function lancamento_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   unrecognized PropertyName/PropertyValue pairs from the
%            command line (see VARARGIN)

% Choose default command line output for lancamento
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes lancamento wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = lancamento_OutputFcn(hObject, eventdata, handles)
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes on button press in ok.
function ok_Callback(hObject, eventdata, handles)
% hObject    handle to ok (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% Entradas Constantes

d = 0.0325*2; % Diâmetro [m]
A = (pi*d^2)/4; % Área seção transversal [m^2]
p = 1.225; % Densidade do ar [kg/m^3] 
Cd = 0.64; % Coeficiente de arrasto
m = 58*10^-3; % Massa [kg]
g = 9.81; % Aceleração da gravidade [m/s^2]

%numerico
t0 = 0; % tempo inicial
tf = 10; % tempo final
dt=0.01; % discretização
t = t0:dt:tf; % vetor tempo

v_vent = [str2double(get(handles.vx_vent,'string')) str2double(get(handles.vy_vent,'string')) str2double(get(handles.vz_vent,'string'))]; % Velocidade do vento

% posições iniciais
sx0=str2double(get(handles.x0,'string')); % posição inicial em x [m]
sy0=str2double(get(handles.y0,'string')); % posição inicial em y [m]
sz0=str2double(get(handles.z0,'string')); % posição inicial em z [m] 

 % velocidades iniciais [m/s]
vx0=str2double(get(handles.vxy0,'string'))*cos(str2double(get(handles.thetaxy0,'string'))*pi/180);
vy0=str2double(get(handles.vxy0,'string'))*sin(str2double(get(handles.thetaxy0,'string'))*pi/180);
vz0=str2double(get(handles.vz0,'string'));
vi=[vx0,vy0,vz0];

% velocidades angulares [rad/s]
wx=str2double(get(handles.wx,'string'));
wy=str2double(get(handles.wy,'string'));
wz=str2double(get(handles.wz,'string')); %negativo top spin e positivo back spin
wi=[wx,wy,wz];

Cl = d*norm(wi)/(2*norm(vi)); % Coeficiente de sustentação

%Vetor Força da gravidade [N]
F_g=[0,-m*g,0];


for i = 1:length(t)
sx(i,1)=sx0;
sy(i,1)=sy0;
sz(i,1)=sz0; 

vx(i,1)=vx0;
vy(i,1)=vy0;
vz(i,1)=vz0;


vi=[vx0,vy0,vz0];

%Forca Magnus
if norm(wi)==0
    F_mag = [0 0 0];
else 
   F_mag=0.5*p*A*Cl*(norm(vi)^2)*cross(wi,vi)/(norm(cross(wi,vi)));
end    

%Força de arrasto
v_rel = vi-v_vent;
F_a=-0.5*p*A*Cd*(norm(v_rel)^2)*(v_rel/(norm(v_rel)));

dvdt= (F_g + F_mag + F_a)/m ;
dvxdt=dvdt(1,1);
dvydt=dvdt(1,2);
dvzdt=dvdt(1,3);

vx0 = vx0 + dvxdt*dt ;   
vy0 = vy0 + dvydt*dt ;  
vz0 = vz0 + dvzdt*dt ;  

vx(i,1)=vx0;
vy(i,1)=vy0;
vz(i,1)=vz0;

sx0 = sx0 + vx0*dt ;   
sy0 = sy0 + vy0*dt ;  
sz0 = sz0 + vz0*dt ;  
if sy0 < d/2
    break
end

sx(i,1)=sx0;
sy(i,1)=sy0;
sz(i,1)=sz0;

end




t = t0:dt:dt*(length(sx)-1); % novo vetor tempo
rede_x = [1189 1189 1189 1189 1189 1189];
rede_y = 0:18.28:91.4;

if get(handles.sup,'value') == get(handles.sup,'max')
    I = imread('Quadra.jpg');
    I = imresize(I,[1200 2500]);
    I = flipud(I);
    imshow(I)
    axis on %this will show you the axis ticks; note the y axis is reversed!
    axis xy
    hold on
    plot(100*sx,100*sz,'ro:')
    axis([0 2500 0 1200])
    title('Tragetória da bola em XZ')
    xlabel('Posição X [cm]')
    ylabel('Posição Z [cm]')
    hold off
else
    plot(100*sx,100*sy,'ro:',rede_x,rede_y,'b-')
%     axis([0 2377 0 500])
    title('Tragetória da bola em XY')
    legend('bola','rede')
    xlabel('Posição X [cm]')
    ylabel('Posição Y [cm]')
end




function x0_Callback(hObject, eventdata, handles)
% hObject    handle to x0 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of x0 as text
%        str2double(get(hObject,'String')) returns contents of x0 as a double


% --- Executes during object creation, after setting all properties.
function x0_CreateFcn(hObject, eventdata, handles)
% hObject    handle to x0 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function y0_Callback(hObject, eventdata, handles)
% hObject    handle to y0 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of y0 as text
%        str2double(get(hObject,'String')) returns contents of y0 as a double


% --- Executes during object creation, after setting all properties.
function y0_CreateFcn(hObject, eventdata, handles)
% hObject    handle to y0 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function z0_Callback(hObject, eventdata, handles)
% hObject    handle to z0 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of z0 as text
%        str2double(get(hObject,'String')) returns contents of z0 as a double


% --- Executes during object creation, after setting all properties.
function z0_CreateFcn(hObject, eventdata, handles)
% hObject    handle to z0 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function vxy0_Callback(hObject, eventdata, handles)
% hObject    handle to vxy0 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of vxy0 as text
%        str2double(get(hObject,'String')) returns contents of vxy0 as a double


% --- Executes during object creation, after setting all properties.
function vxy0_CreateFcn(hObject, eventdata, handles)
% hObject    handle to vxy0 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function thetaxy0_Callback(hObject, eventdata, handles)
% hObject    handle to thetaxy0 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of thetaxy0 as text
%        str2double(get(hObject,'String')) returns contents of thetaxy0 as a double


% --- Executes during object creation, after setting all properties.
function thetaxy0_CreateFcn(hObject, eventdata, handles)
% hObject    handle to thetaxy0 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function vz0_Callback(hObject, eventdata, handles)
% hObject    handle to vz0 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of vz0 as text
%        str2double(get(hObject,'String')) returns contents of vz0 as a double


% --- Executes during object creation, after setting all properties.
function vz0_CreateFcn(hObject, eventdata, handles)
% hObject    handle to vz0 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function wx_Callback(hObject, eventdata, handles)
% hObject    handle to wx (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of wx as text
%        str2double(get(hObject,'String')) returns contents of wx as a double


% --- Executes during object creation, after setting all properties.
function wx_CreateFcn(hObject, eventdata, handles)
% hObject    handle to wx (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function wy_Callback(hObject, eventdata, handles)
% hObject    handle to wy (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of wy as text
%        str2double(get(hObject,'String')) returns contents of wy as a double


% --- Executes during object creation, after setting all properties.
function wy_CreateFcn(hObject, eventdata, handles)
% hObject    handle to wy (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function wz_Callback(hObject, eventdata, handles)
% hObject    handle to wz (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of wz as text
%        str2double(get(hObject,'String')) returns contents of wz as a double


% --- Executes during object creation, after setting all properties.
function wz_CreateFcn(hObject, eventdata, handles)
% hObject    handle to wz (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function vx_vent_Callback(hObject, eventdata, handles)
% hObject    handle to vx_vent (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of vx_vent as text
%        str2double(get(hObject,'String')) returns contents of vx_vent as a double


% --- Executes during object creation, after setting all properties.
function vx_vent_CreateFcn(hObject, eventdata, handles)
% hObject    handle to vx_vent (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function vy_vent_Callback(hObject, eventdata, handles)
% hObject    handle to vy_vent (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of vy_vent as text
%        str2double(get(hObject,'String')) returns contents of vy_vent as a double


% --- Executes during object creation, after setting all properties.
function vy_vent_CreateFcn(hObject, eventdata, handles)
% hObject    handle to vy_vent (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function vz_vent_Callback(hObject, eventdata, handles)
% hObject    handle to vz_vent (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of vz_vent as text
%        str2double(get(hObject,'String')) returns contents of vz_vent as a double


% --- Executes during object creation, after setting all properties.
function vz_vent_CreateFcn(hObject, eventdata, handles)
% hObject    handle to vz_vent (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in sup.
function sup_Callback(hObject, eventdata, handles)
% hObject    handle to sup (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of sup


% --- Executes on button press in lat.
function lat_Callback(hObject, eventdata, handles)
% hObject    handle to lat (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of lat


% --- Executes during object creation, after setting all properties.
function uibuttongroup2_CreateFcn(hObject, eventdata, handles)
% hObject    handle to uibuttongroup2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called
