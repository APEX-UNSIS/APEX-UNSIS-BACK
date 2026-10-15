##  Diagramas Visuales del Sistema de Autenticación

###  Flujo de Login

```

   FRONTEND  
             
  [Usuario]  
  [Password] 
             
  [Login]    

       
        POST /api/v1/auth/login
        { user: "admin", password: "admin123" }
       

         BACKEND - auth.py            
                                      
  1. Recibe credenciales              
  2. Llama a authenticate_user()      

       
       

    UsuarioService.authenticate_user  
                                      
  1. Busca usuario en BD              
  2. Verifica contraseña con bcrypt   
  3. Actualiza last_login             
  4. Retorna usuario si es válido     

       
        ¿Válido?
       
    
      ¿?  
    
        
  NO      SI
        
        
    
   401   Generar JWT Token    
         create_access_token()
    
                 
                 
          
            Token + User Data      
                                   
            {                      
              "token": "eyJhbG...",
              "user": {            
                "id_usuario": "...",
                "rol": "admin",    
                ...                
              }                    
            }                      
          
                   
                   
            
               FRONTEND   
                          
             Guarda token 
             en localStorage
            
```

###  Flujo de Petición Protegida

```

   FRONTEND  
             
 Token en    
 localStorage

       
        GET /api/v1/solicitudes
        Header: Authorization: Bearer eyJhbG...
       

    ENDPOINT PROTEGIDO                
                                      
  @router.get("/solicitudes")         
  def get_solicitudes(                
    current_user = Depends(           
      get_current_active_user         
    )                                 
  ):                                  

       
        Ejecuta dependencia
       

   get_current_active_user()          
   (en dependencies.py)               
                                      
  1. Llama a get_current_user()       

       
       

   get_current_user()                 
   (en auth.py)                       
                                      
  1. Extrae token del header          
  2. Decodifica JWT                   
  3. Verifica firma y expiración      
  4. Obtiene id_usuario del payload   
  5. Busca usuario en BD              

       
        ¿Token válido?
       
    
      ¿?  
    
        
  NO      SI
        
        
    
   401   Retorna Usuario      
         UsuarioResponse      
    
                 
                 
          
            current_user disponible
            en el endpoint         
                                   
            - current_user.rol     
            - current_user.id      
            - current_user.carrera 
          
                   
                    ¿Tiene permiso?
                   
                
                  ¿?  
                
                    
              NO      SI
                    
                    
                
               403   Ejecuta lógica  
                     del endpoint    
                
                               
                               
                        
                          RESPUESTA   
                                      
                         { data: ... }
                        
```

###  Verificación por Roles

```

   PETICIÓN CON TOKEN                 

       
       

   Depends(require_admin)             

       
        1. Obtiene current_user
       

   Verifica: current_user.rol         

       
       
    
     ¿Es "admin"?     
    
                    
   NO                SI
                    
                    
         
   403        PERMITE 
              ACCESO  
         
```

###  Ciclo de Vida del Token

```

   LOGIN     
  EXITOSO    

       
       

   TOKEN GENERADO                     
                                      
   Expira en: 30 días (por defecto)   
   Contiene: { sub, rol, exp }        

       
       

   FRONTEND GUARDA TOKEN              
   localStorage.setItem('token', ...) 

       
        Usar en cada petición
       

   PETICIONES AUTENTICADAS            
   Header: Authorization: Bearer ...  

       
        Durante 30 días
       

   TOKEN EXPIRA                       
   Backend retorna 401                

       
       

   FRONTEND ELIMINA TOKEN             
   Redirige a login                   

```

###  Arquitectura de Archivos

```
APEX-UNSIS-BACK/

 app/
  
   api/v1/endpoints/
     auth.py 
      • /login             AUTENTICACIÓN
      • /me               
      • get_current_user()
     ejemplo_auth.py 
  
   dependencies.py 
    • get_current_active_user MIDDLEWARE
    • require_admin          DE
    • require_roles          PROTECCIÓN
    • require_jefe_or_admin 
                            
   services/               
     UsuarioService.py 
       • authenticate_user() LÓGICA DE
       • verify_password()   NEGOCIO
       • get_password_hash()
                            
   repositories/           
     UsuarioRepository.py
       • get_by_username_or_id ACCESO A
       • get_by_id_usuario   DATOS
       • get_by_rol          
                            
   models/                 
     Usuario.py 
       • id_usuario          MODELO
       • contraseña (hash)   DE DATOS
       • rol, email, etc    
                            
   schemas/                
      UsuarioSchema.py 
        • UsuarioLogin
        • UsuarioResponse
        • TokenResponse

 generar_hashes.py 
 insertar_usuarios_prueba.sql UTILIDADES
 test_auth.py 
 ejemplo_frontend_login.html
```

###  Roles y Permisos

```

                   ADMIN                      
  • Acceso total                              
  • Crear/editar/eliminar usuarios            
  • Ver todas las carreras                    
  • Aprobar/rechazar solicitudes              
  • Configuración del sistema                 

                
                 Puede hacer todo lo que hace JEFE
                

                   JEFE                       
  • Ver datos de SU carrera                   
  • Aprobar/rechazar solicitudes de su carrera
  • Asignar sinodales                         
  • Gestionar grupos de su carrera            

                
                 Acceso limitado comparado con ADMIN
                

                SERVICIOS                     
  • Ver solicitudes asignadas                 
  • Actualizar estados de solicitudes         
  • Ver calendarios de exámenes               
  • Asignar aulas                             

```

###  Seguridad de Contraseñas

```

  CONTRASEÑA     
  "admin123"     

         
         

  bcrypt.gensalt()           
  Genera salt aleatorio      

         
         

  bcrypt.hashpw()            
  password + salt            

         
         

  HASH GUARDADO EN BD                    
  $2b$12$LQv3c1yqBWVHxkd0LHAkCOYz...    
  (60 caracteres)                        


VERIFICACIÓN:
   
 Password            Hash de BD             
 ingresado           $2b$12$LQv3c1y...     
   
                              
         
                    
         
           bcrypt.checkpw()    
         
                    
                    
              
                Match  
               o         
                No Match
              
```

###  Integración Frontend-Backend

```

              FRONTEND (React/Vue/HTML)      

               
                1. Usuario hace login
               
        
          fetch()    
          POST login 
        
               
               

              BACKEND (FastAPI)               
              /api/v1/auth/login              

               
                2. Valida y genera token
               
        
           TOKEN     
         + User Data 
        
               
               

              FRONTEND                        
  localStorage.setItem('token', data.token)   

               
                3. Peticiones subsecuentes
               
        
          fetch()    
          + Header   
          Bearer ... 
        
               
               

              BACKEND                         
  Valida token → Ejecuta endpoint             

               
                4. Retorna datos
               
        
          Respuesta  
          JSON       
        
               
               

              FRONTEND                        
  Muestra datos al usuario                    

```

---

##  Leyenda

```

       = Proceso


   
        = Flujo de datos


     = Resultado exitoso



     = Error



  ?    = Decisión/Validación

```
