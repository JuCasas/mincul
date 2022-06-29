DROP TRIGGER if EXISTS TR_INSERT_PATRIMONIO
ON patrimonios_patrimonio;

DROP TRIGGER if exists TR_INSERT_INSTITUCION
ON patrimonios_institucion;

DROP FUNCTION if exists SP_TR_INSERT_PATRIMONIO;

DROP FUNCTION if exists SP_TR_INSERT_INSTITUCION;


Create or replace function SP_TR_INSERT_INSTITUCION() returns Trigger
as
$$
Declare
begin
Insert into patrimonios_puntogeografico(nombre,institucion_id,tipo)
VALUES (new.nombre,new.id,'2');
return new;
end
$$
LANGUAGE plpgsql;

Create or replace function SP_TR_INSERT_PATRIMONIO() returns Trigger
as
$$
Declare
begin
	    IF new."tipoPatrimonio" = '1' or new."tipoPatrimonio" = '2' then
		Insert into patrimonios_puntogeografico(nombre,patrimonio_id,tipo) VALUES (new."nombreTituloDemoninacion",new.id,'1');
	END IF;
return new;
end
$$
LANGUAGE plpgsql;

Create Trigger TR_INSERT_INSTITUCION after insert on patrimonios_institucion
for each row
execute procedure SP_TR_INSERT_INSTITUCION();

Create  Trigger TR_INSERT_PATRIMONIO after insert on patrimonios_patrimonio
for each row
execute procedure SP_TR_INSERT_PATRIMONIO();