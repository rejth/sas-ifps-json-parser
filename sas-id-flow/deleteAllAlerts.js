const pgp = require("pg-promise")();

pgp.pg.defaults.ssl = true;

const user = "dbmsowner",
    pass = "hrgauiUWU7E8uew8Oor3wHPgalV3N92",
    ip = "ruspfraudvi.rus.sas.com",
    port = "5432",
    dbName = "banff",
    db = pgp(`postgres://${user}:${pass}@${ip}:${port}/${dbName}`);

let i = 0;
const query = (q) => new Promise((response, reject) => {
    db.none(q)
        .then(() => {
            console.log(++i + ". Successfully: " + q);
            response();
        })
        .catch((error) => {
            console.log(error);
            reject();
        });
});

async function run() {
    await query("delete from svi_alerts.tdc_contributing_object");
    await query("delete from svi_alerts.tdc_scenario_fired_event");
    await query("update svi_alerts.tdc_alerting_event set alert_id = null");
    await query("delete from svi_alerts.tdc_alert");
    await query("delete from svi_alerts.tdc_alert_action");
    await query("delete from svi_alerts.tdc_replicated_object");
    await query("delete from svi_alerts.tdc_alerting_event");
    await query("update fdhdata.dh_document_sheet_cell set document_sheet_id = null where document_sheet_id in (select document_sheet_id from fdhdata.dh_document_sheet where document_type_nm = 'alerts' )");
    await query("delete from fdhdata.dh_document_reference_cell where document_sheet_cell_id in (select document_sheet_cell_id from fdhdata.dh_document_sheet_cell where document_sheet_id is null)");
    await query("delete from fdhdata.dh_entity_reference_cell where document_sheet_cell_id in (select document_sheet_cell_id from fdhdata.dh_document_sheet_cell where document_sheet_id is null)");
    await query("delete from fdhdata.dh_document_sheet_cell where document_sheet_id is null");
    await query("delete from fdhdata.dh_document_sheet where document_type_nm = 'alerts'");
}
run();
