from flask import Blueprint
from flask_restful import Api

from application.estilos.controladores.chatController import ChatController, HistorialWithCedulaAllComplete, InterpretacionChatController, LimpiarSesionesController, MensajeController
from application.estilos.controladores.rolController import RolController, RolWithIdController
from application.estilos.controladores.personaController import NotasPorCursoMateriaController, PersonaController, PersonaWithIdController
from application.estilos.controladores.cursoController import CursoController, CursoWithIdController, CursoWithIdUsuario
from application.estilos.controladores.usuarioController import UsuarioController, UsuarioWithIdController, UsuarioWithCedula,UsuarioCedulas, UsuarioWithRolCodigo
from application.estilos.controladores.encuestaController import EncuestToDeleteAllEncuestaRelationed, EncuestaController, EncuestaWithIdController,EncuestaRoutesPersonalized
from application.estilos.controladores.reglasCalculoController import ReglasCalculoController, ReglasCalculoWithIdController
from application.estilos.controladores.estiloController import EstiloController, EstiloWithIdController, EstiloWithIdEncuesta, EstiloWithIdActualizarCampos
from application.estilos.controladores.preguntasController import PreguntaController, PreguntaWithIdController
from application.estilos.controladores.opcionController import OpcionController, OpcionWithIdController
from application.estilos.controladores.respuestaController import RespuestaController, RespuestaWithIdController, RespuestaWithasi_id
from application.estilos.controladores.asignacionController import AsignacionController, AsignacionTerminada, AsignacionWithEncuestaId, AsignacionWithIdController, AsignacionWithUsuarioDocenteId,AsignacionWithUsuarioId,AsignacionTestWithId,AsignacionWithCursoId,AsignacionWithCursoIdMaterias, AsignacionesDeleteController
from application.estilos.controladores.historialController import HistorialByCursoMateriaEncuestaController, HistorialController, HistorialWithIdController,HistorialWithIdAsignacion, HistorialByCursoMateriaController
from application.estilos.controladores.recalificarController import RecalificarTest, RecalificarTestApp
from application.estilos.controladores.credencialesApiController import CredencialesAPIController,CredencialesWithcredIdController
from application.estilos.controladores.authController import LoginController,LogoutController
from application.estilos.controladores.materiaController import MateriaController, MateriaEstudianteController
from application.estilos.controladores.parcialController import ParcialController
from application.estilos.controladores.parcialController import ParcialWithIdController
from application.estilos.controladores.notaController import NotaController
from application.estilos.controladores.notaController import NotaWithIdController
from application.estilos.controladores.promptController import PromptController ,PromptWithIdController
from application.constant.constants import Constants


routes_estilos_v1 = Blueprint('routes_estilos_v1', __name__)
api = Api(routes_estilos_v1)

#**RUTAS**

#AUTHENTICATION
api.add_resource(LoginController, f'{Constants.API}/auth/login', endpoint='auth_login_resource')
api.add_resource(LogoutController, f'{Constants.API}/auth/logout/<int:usu_id>', endpoint='auth_logout_resource')

#ROLES
api.add_resource(RolController, f'{Constants.API}/rol', endpoint='rol_resource')
api.add_resource(RolWithIdController, f'{Constants.API}/rol/<string:rol_id>', endpoint='rol_id_resource')

#PERSONAS
api.add_resource(PersonaController, f'{Constants.API}/persona', endpoint='persona_resource')
api.add_resource(PersonaWithIdController,  f'{Constants.API}/persona/<string:per_cedula>', endpoint='persona_cedula_resource')
api.add_resource(NotasPorCursoMateriaController,f'{Constants.API}/personas/curso/notas/<int:cur_id>/<int:mat_id>', endpoint='notas_por_curso_materia')

#CURSOS
api.add_resource(CursoController,  f'{Constants.API}/curso', endpoint='curso_resource')
api.add_resource(CursoWithIdController,  f'{Constants.API}/curso/<int:cur_id>', endpoint='curso_id_resource')
api.add_resource(CursoWithIdUsuario,  f'{Constants.API}/curso/usuario/<int:usu_id>', endpoint='usu_id_resource')

#USUARIO
api.add_resource(UsuarioController,  f'{Constants.API}/usuario', endpoint='usuario_resource')
api.add_resource(UsuarioWithCedula, f'{Constants.API}/usuario/cedula/<string:per_cedula>',endpoint='get_by_cedula')
api.add_resource(UsuarioWithIdController,  f'{Constants.API}/usuario/<int:usu_id>', endpoint='usuario_id_resource')
api.add_resource(UsuarioCedulas,  f'{Constants.API}/usuario-cedulas', endpoint='usuario_cedulas')
api.add_resource(UsuarioWithRolCodigo, f'{Constants.API}/usuario/rol/codigo/<string:rol_codigo>',endpoint='get_by_rol_codigo')

#ENCUESTA
api.add_resource(EncuestaController,  f'{Constants.API}/encuesta', endpoint='encuesta_resource')
api.add_resource(EncuestaRoutesPersonalized,  f'{Constants.API}/encuesta/detalles/<int:enc_id>', endpoint='get_with_details')
api.add_resource(EncuestaWithIdController,  f'{Constants.API}/encuesta/<int:enc_id>', endpoint='encuesta_id_resource')
api.add_resource(EncuestToDeleteAllEncuestaRelationed,  f'{Constants.API}/encuesta/delete/all/<int:enc_id>', endpoint='encuesta_id_delete_all_resource')

#REGLAS DE CALCULO
api.add_resource(ReglasCalculoController,  f'{Constants.API}/reglas', endpoint='reglas_resource')
api.add_resource(ReglasCalculoWithIdController,  f'{Constants.API}/reglas/<int:reg_id>', endpoint='reglas_id_resource')

#ESTILO
api.add_resource(EstiloController,  f'{Constants.API}/estilo', endpoint='estilos_resource')
api.add_resource(EstiloWithIdEncuesta,  f'{Constants.API}/estilo/encuesta/<int:enc_id>', endpoint='enc_id_resource')
api.add_resource(EstiloWithIdController,  f'{Constants.API}/estilo/<int:est_id>', endpoint='estilos_id_resource')
api.add_resource(EstiloWithIdActualizarCampos,  f'{Constants.API}/estilo/actualizar/<int:est_id>', endpoint='estilos_actualizar_id_resource')

#PREGUNTA
api.add_resource(PreguntaController,  f'{Constants.API}/pregunta', endpoint='preguntas_resource')
api.add_resource(PreguntaWithIdController,  f'{Constants.API}/pregunta/<int:pre_id>', endpoint='preguntas_id_resource')

#OPCION
api.add_resource(OpcionController,  f'{Constants.API}/opcion', endpoint='opciones_resource')
api.add_resource(OpcionWithIdController,  f'{Constants.API}/opcion/<int:opc_id>', endpoint='opciones_id_resource')

#RESPUESTA
api.add_resource(RespuestaController,  f'{Constants.API}/respuesta', endpoint='respuestas_resource')
api.add_resource(RespuestaWithIdController,  f'{Constants.API}/respuesta/<int:res_id>', endpoint='respuestas_id_resource')
api.add_resource(RespuestaWithasi_id,  f'{Constants.API}/respuesta/asignacion/<int:asi_id>', endpoint='respuestas_asi_id_resource')

#ASIGNACIONES
api.add_resource(AsignacionController,  f'{Constants.API}/asignacion', endpoint='asignaciones_resource')
api.add_resource(AsignacionWithIdController,  f'{Constants.API}/asignacion/<int:asi_id>', endpoint='asignaciones_id_resource')
api.add_resource(AsignacionWithUsuarioId,  f'{Constants.API}/asignacion/usuario/<int:usu_id>', endpoint='asignacion_with_usuario_id')
api.add_resource(AsignacionTerminada,  f'{Constants.API}/asignacion/usuario/terminada/<int:asi_id>', endpoint='asignacion_terminada_with_asignacion_id')
api.add_resource(AsignacionWithUsuarioDocenteId,  f'{Constants.API}/asignacion/usuario/docente/<int:usu_id>', endpoint='asignacion_with_usuario_docente_id')
api.add_resource(AsignacionWithCursoId,  f'{Constants.API}/asignacion/curso/<int:cur_id>', endpoint='asignacion_with_curso_id')
api.add_resource(AsignacionTestWithId,  f'{Constants.API}/asignacion/test/<int:asi_id>', endpoint='asignacion_test_with_asi_id')
api.add_resource(AsignacionWithEncuestaId,  f'{Constants.API}/asignacion/encuesta/<int:enc_id>', endpoint='asignacion_encuesta_with_enc_id')
api.add_resource(AsignacionWithCursoIdMaterias ,  f'{Constants.API}/asignacion/materia/<int:cur_id>', endpoint='asignacion_materia_with_cur_id')
api.add_resource(AsignacionesDeleteController ,  f'{Constants.API}/asignaciones/eliminar', endpoint='asignaciones/eliminar')

#HISTORIAL
api.add_resource(HistorialController,  f'{Constants.API}/historial', endpoint='historial_resource')
api.add_resource(HistorialWithIdController,  f'{Constants.API}/historial/<int:reg_id>', endpoint='historial_id_resource')
api.add_resource(HistorialWithIdAsignacion,  f'{Constants.API}/historial/asignacion', endpoint='historial_id_asignacion')
api.add_resource(HistorialByCursoMateriaController,  f'{Constants.API}/historial/curso/materia', endpoint='historial_id_curso_materia')
api.add_resource(HistorialByCursoMateriaEncuestaController,  f'{Constants.API}/historial/curso/materia/encuesta', endpoint='historial_id_curso_materia_encuesta')

#MATERIA
api.add_resource(MateriaController,  f'{Constants.API}/materia', endpoint='materia_resource')
api.add_resource(MateriaEstudianteController,  f'{Constants.API}/materia/estudiantes', endpoint='materia_estudiantes_resource')

#RECALIFICAR
api.add_resource(RecalificarTest,  f'{Constants.API}/recalificar', endpoint='recalificar_resource')
api.add_resource(RecalificarTestApp,  f'{Constants.API}/recalificar/app', endpoint='recalificar_app_resource')

#CREDENCIALES
api.add_resource(CredencialesAPIController,  f'{Constants.API}/credencial', endpoint='credencialApi_resource')
api.add_resource(CredencialesWithcredIdController,  f'{Constants.API}/credencial/<int:cred_id>', endpoint='credencialApiWithCredId_resource')

#PARCIAL
api.add_resource(ParcialController,  f'{Constants.API}/parcial', endpoint='parcial_resource')
api.add_resource(ParcialWithIdController,  f'{Constants.API}/parcial/<int:par_id>', endpoint='parcialWithCredId_resource')

#NOTA
api.add_resource(NotaController,  f'{Constants.API}/nota', endpoint='nota_resource')
api.add_resource(NotaWithIdController,  f'{Constants.API}/nota/<int:not_id>', endpoint='notaWithIdController_resource')

# Prompt
api.add_resource(PromptController,  f'{Constants.API}/prompt', endpoint='prompt_resource')
api.add_resource(PromptWithIdController,  f'{Constants.API}/prompt/<int:pro_id>', endpoint='promptWithIdController_resource')

#CHAT
api.add_resource(ChatController, f'{Constants.API}/chat', endpoint='chat_resource')
api.add_resource(MensajeController, f'{Constants.API}/mensaje', endpoint='mensaje_resource')
api.add_resource(LimpiarSesionesController, f'{Constants.API}/sesiones/limpiar', endpoint='limpiar_sesiones_resource')
api.add_resource(HistorialWithCedulaAllComplete, f'{Constants.API}/estudiante/all/indo/<string:est_cedula>', endpoint='info_all_estudiante')
api.add_resource(InterpretacionChatController, f'{Constants.API}/interpretacion/encuesta', endpoint='interpretacion_encuesta')
