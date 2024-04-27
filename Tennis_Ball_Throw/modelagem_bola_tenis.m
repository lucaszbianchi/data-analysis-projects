clc
clear all

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
dt=0.008; % discretização
t = t0:dt:tf; % vetor tempo

v_vent = [0 0 0]; % Velocidade do vento

% posições iniciais
sx0=-8; % posição inicial em x [m]
sy0=0.5; % posição inicial em y [m]
sz0=5.4; % posição inicial em z [m] 

% velocidades iniciais [m/s]
vxy0 = 4000;
theta0 = 20;
vx0=vxy0*cos(theta0*pi/180);
vy0=vxy0*sin(theta0*pi/180);
vz0=0;
vi=[vx0,vy0,vz0];

% velocidades angulares [rad/s]
wx=0;
wy=0;
wz=0; %negativo top spin e positivo back spin
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

figure(1)
plot(100*sx,100*sy,'ro:',rede_x,rede_y,'b-')
axis([0 2377 0 300])
title('Tragetória da bola em XY')
legend('bola','rede')
xlabel('Posição X [cm]')
ylabel('Posição Y [cm]')

figure(2)
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