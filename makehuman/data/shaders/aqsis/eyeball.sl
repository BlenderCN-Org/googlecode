






surface
eyeball ( float Ks = 3;
          float Kd = 1;
          float Ka = 0.2;
          string colortexture = "";  
          float roughness = .02;
	      color specularcolor = 1;
          color opacity = 0.01;
     )
{    
    normal Nf = faceforward (normalize(N),I); 
    vector V = -normalize(I);
    color eyetexture = 1;
    float angle_ramp = (max(0,(1-( V.Nf))))/4;
    
    if (colortexture != "")
	    eyetexture = color texture (colortexture);   
       
    color Spec = Ks*specular(Nf,-normalize(I),roughness);
    
    Oi = 1;
    Ci = eyetexture * (Ka*ambient() + Kd*diffuse(Nf)) + specularcolor * Spec;
}
