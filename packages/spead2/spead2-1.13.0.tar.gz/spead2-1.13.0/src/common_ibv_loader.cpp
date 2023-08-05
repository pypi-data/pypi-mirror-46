#ifndef _GNU_SOURCE
# define _GNU_SOURCE
#endif
#include <spead2/common_features.h>

#if SPEAD2_USE_IBV

#include <spead2/common_ibv_loader.h>
#include <spead2/common_ibv_loader_utils.h>
#include <spead2/common_logging.h>
#include <mutex>
#include <exception>

namespace spead2
{

static std::once_flag init_once;
static std::exception_ptr init_result;

void ibv_ack_cq_events_stub(struct ibv_cq *cq, unsigned int nevents)
{
    (void) cq;
    (void) nevents;
    ibv_loader_stub(init_result);
}
struct ibv_pd *ibv_alloc_pd_stub(struct ibv_context *context)
{
    (void) context;
    ibv_loader_stub(init_result);
}
int ibv_close_device_stub(struct ibv_context *context)
{
    (void) context;
    ibv_loader_stub(init_result);
}
struct ibv_comp_channel *ibv_create_comp_channel_stub(struct ibv_context *context)
{
    (void) context;
    ibv_loader_stub(init_result);
}
struct ibv_cq *ibv_create_cq_stub(struct ibv_context *context, int cqe, void *cq_context, struct ibv_comp_channel *channel, int comp_vector)
{
    (void) context;
    (void) cqe;
    (void) cq_context;
    (void) channel;
    (void) comp_vector;
    ibv_loader_stub(init_result);
}
struct ibv_qp *ibv_create_qp_stub(struct ibv_pd *pd, struct ibv_qp_init_attr *qp_init_attr)
{
    (void) pd;
    (void) qp_init_attr;
    ibv_loader_stub(init_result);
}
int ibv_dealloc_pd_stub(struct ibv_pd *pd)
{
    (void) pd;
    ibv_loader_stub(init_result);
}
int ibv_dereg_mr_stub(struct ibv_mr *mr)
{
    (void) mr;
    ibv_loader_stub(init_result);
}
int ibv_destroy_comp_channel_stub(struct ibv_comp_channel *channel)
{
    (void) channel;
    ibv_loader_stub(init_result);
}
int ibv_destroy_cq_stub(struct ibv_cq *cq)
{
    (void) cq;
    ibv_loader_stub(init_result);
}
int ibv_destroy_qp_stub(struct ibv_qp *qp)
{
    (void) qp;
    ibv_loader_stub(init_result);
}
void ibv_free_device_list_stub(struct ibv_device **list)
{
    (void) list;
    ibv_loader_stub(init_result);
}
int ibv_get_cq_event_stub(struct ibv_comp_channel *channel, struct ibv_cq **cq, void **cq_context)
{
    (void) channel;
    (void) cq;
    (void) cq_context;
    ibv_loader_stub(init_result);
}
uint64_t ibv_get_device_guid_stub(struct ibv_device *device)
{
    (void) device;
    ibv_loader_stub(init_result);
}
struct ibv_device **ibv_get_device_list_stub(int *num_devices)
{
    (void) num_devices;
    ibv_loader_stub(init_result);
}
struct ibv_context *ibv_open_device_stub(struct ibv_device *device)
{
    (void) device;
    ibv_loader_stub(init_result);
}
int ibv_modify_qp_stub(struct ibv_qp *qp, struct ibv_qp_attr *attr, int attr_mask)
{
    (void) qp;
    (void) attr;
    (void) attr_mask;
    ibv_loader_stub(init_result);
}
int ibv_query_device_stub(struct ibv_context *context, struct ibv_device_attr *device_attr)
{
    (void) context;
    (void) device_attr;
    ibv_loader_stub(init_result);
}
struct ibv_mr *ibv_reg_mr_stub(struct ibv_pd *pd, void *addr, size_t length, int access)
{
    (void) pd;
    (void) addr;
    (void) length;
    (void) access;
    ibv_loader_stub(init_result);
}
int rdma_bind_addr_stub(struct rdma_cm_id *id, struct sockaddr *addr)
{
    (void) id;
    (void) addr;
    ibv_loader_stub(init_result);
}
struct rdma_event_channel *rdma_create_event_channel_stub(void)
{
    ibv_loader_stub(init_result);
}
int rdma_create_id_stub(struct rdma_event_channel *channel, struct rdma_cm_id **id, void *context, enum rdma_port_space ps)
{
    (void) channel;
    (void) id;
    (void) context;
    (void) ps;
    ibv_loader_stub(init_result);
}
void rdma_destroy_event_channel_stub(struct rdma_event_channel *channel)
{
    (void) channel;
    ibv_loader_stub(init_result);
}
int rdma_destroy_id_stub(struct rdma_cm_id *id)
{
    (void) id;
    ibv_loader_stub(init_result);
}

void (*ibv_ack_cq_events)(struct ibv_cq *cq, unsigned int nevents) = ibv_ack_cq_events_stub;
struct ibv_pd *(*ibv_alloc_pd)(struct ibv_context *context) = ibv_alloc_pd_stub;
int (*ibv_close_device)(struct ibv_context *context) = ibv_close_device_stub;
struct ibv_comp_channel *(*ibv_create_comp_channel)(struct ibv_context *context) = ibv_create_comp_channel_stub;
struct ibv_cq *(*ibv_create_cq)(struct ibv_context *context, int cqe, void *cq_context, struct ibv_comp_channel *channel, int comp_vector) = ibv_create_cq_stub;
struct ibv_qp *(*ibv_create_qp)(struct ibv_pd *pd, struct ibv_qp_init_attr *qp_init_attr) = ibv_create_qp_stub;
int (*ibv_dealloc_pd)(struct ibv_pd *pd) = ibv_dealloc_pd_stub;
int (*ibv_dereg_mr)(struct ibv_mr *mr) = ibv_dereg_mr_stub;
int (*ibv_destroy_comp_channel)(struct ibv_comp_channel *channel) = ibv_destroy_comp_channel_stub;
int (*ibv_destroy_cq)(struct ibv_cq *cq) = ibv_destroy_cq_stub;
int (*ibv_destroy_qp)(struct ibv_qp *qp) = ibv_destroy_qp_stub;
void (*ibv_free_device_list)(struct ibv_device **list) = ibv_free_device_list_stub;
int (*ibv_get_cq_event)(struct ibv_comp_channel *channel, struct ibv_cq **cq, void **cq_context) = ibv_get_cq_event_stub;
uint64_t (*ibv_get_device_guid)(struct ibv_device *device) = ibv_get_device_guid_stub;
struct ibv_device **(*ibv_get_device_list)(int *num_devices) = ibv_get_device_list_stub;
struct ibv_context *(*ibv_open_device)(struct ibv_device *device) = ibv_open_device_stub;
int (*ibv_modify_qp)(struct ibv_qp *qp, struct ibv_qp_attr *attr, int attr_mask) = ibv_modify_qp_stub;
int (*ibv_query_device)(struct ibv_context *context, struct ibv_device_attr *device_attr) = ibv_query_device_stub;
struct ibv_mr *(*ibv_reg_mr)(struct ibv_pd *pd, void *addr, size_t length, int access) = ibv_reg_mr_stub;
int (*rdma_bind_addr)(struct rdma_cm_id *id, struct sockaddr *addr) = rdma_bind_addr_stub;
struct rdma_event_channel *(*rdma_create_event_channel)(void) = rdma_create_event_channel_stub;
int (*rdma_create_id)(struct rdma_event_channel *channel, struct rdma_cm_id **id, void *context, enum rdma_port_space ps) = rdma_create_id_stub;
void (*rdma_destroy_event_channel)(struct rdma_event_channel *channel) = rdma_destroy_event_channel_stub;
int (*rdma_destroy_id)(struct rdma_cm_id *id) = rdma_destroy_id_stub;

static void reset_stubs()
{
    ibv_ack_cq_events = ibv_ack_cq_events_stub;
    ibv_alloc_pd = ibv_alloc_pd_stub;
    ibv_close_device = ibv_close_device_stub;
    ibv_create_comp_channel = ibv_create_comp_channel_stub;
    ibv_create_cq = ibv_create_cq_stub;
    ibv_create_qp = ibv_create_qp_stub;
    ibv_dealloc_pd = ibv_dealloc_pd_stub;
    ibv_dereg_mr = ibv_dereg_mr_stub;
    ibv_destroy_comp_channel = ibv_destroy_comp_channel_stub;
    ibv_destroy_cq = ibv_destroy_cq_stub;
    ibv_destroy_qp = ibv_destroy_qp_stub;
    ibv_free_device_list = ibv_free_device_list_stub;
    ibv_get_cq_event = ibv_get_cq_event_stub;
    ibv_get_device_guid = ibv_get_device_guid_stub;
    ibv_get_device_list = ibv_get_device_list_stub;
    ibv_open_device = ibv_open_device_stub;
    ibv_modify_qp = ibv_modify_qp_stub;
    ibv_query_device = ibv_query_device_stub;
    ibv_reg_mr = ibv_reg_mr_stub;
    rdma_bind_addr = rdma_bind_addr_stub;
    rdma_create_event_channel = rdma_create_event_channel_stub;
    rdma_create_id = rdma_create_id_stub;
    rdma_destroy_event_channel = rdma_destroy_event_channel_stub;
    rdma_destroy_id = rdma_destroy_id_stub;
}

static void init()
{
    try
    {
        dl_handle librdmacm("librdmacm.so.1");
        dl_handle libibverbs("libibverbs.so.1");
        ibv_ack_cq_events = reinterpret_cast<void (*)(struct ibv_cq *cq, unsigned int nevents)>(
            libibverbs.sym("ibv_ack_cq_events"));
        ibv_alloc_pd = reinterpret_cast<struct ibv_pd *(*)(struct ibv_context *context)>(
            libibverbs.sym("ibv_alloc_pd"));
        ibv_close_device = reinterpret_cast<int (*)(struct ibv_context *context)>(
            libibverbs.sym("ibv_close_device"));
        ibv_create_comp_channel = reinterpret_cast<struct ibv_comp_channel *(*)(struct ibv_context *context)>(
            libibverbs.sym("ibv_create_comp_channel"));
        ibv_create_cq = reinterpret_cast<struct ibv_cq *(*)(struct ibv_context *context, int cqe, void *cq_context, struct ibv_comp_channel *channel, int comp_vector)>(
            libibverbs.sym("ibv_create_cq"));
        ibv_create_qp = reinterpret_cast<struct ibv_qp *(*)(struct ibv_pd *pd, struct ibv_qp_init_attr *qp_init_attr)>(
            libibverbs.sym("ibv_create_qp"));
        ibv_dealloc_pd = reinterpret_cast<int (*)(struct ibv_pd *pd)>(
            libibverbs.sym("ibv_dealloc_pd"));
        ibv_dereg_mr = reinterpret_cast<int (*)(struct ibv_mr *mr)>(
            libibverbs.sym("ibv_dereg_mr"));
        ibv_destroy_comp_channel = reinterpret_cast<int (*)(struct ibv_comp_channel *channel)>(
            libibverbs.sym("ibv_destroy_comp_channel"));
        ibv_destroy_cq = reinterpret_cast<int (*)(struct ibv_cq *cq)>(
            libibverbs.sym("ibv_destroy_cq"));
        ibv_destroy_qp = reinterpret_cast<int (*)(struct ibv_qp *qp)>(
            libibverbs.sym("ibv_destroy_qp"));
        ibv_free_device_list = reinterpret_cast<void (*)(struct ibv_device **list)>(
            libibverbs.sym("ibv_free_device_list"));
        ibv_get_cq_event = reinterpret_cast<int (*)(struct ibv_comp_channel *channel, struct ibv_cq **cq, void **cq_context)>(
            libibverbs.sym("ibv_get_cq_event"));
        ibv_get_device_guid = reinterpret_cast<uint64_t (*)(struct ibv_device *device)>(
            libibverbs.sym("ibv_get_device_guid"));
        ibv_get_device_list = reinterpret_cast<struct ibv_device **(*)(int *num_devices)>(
            libibverbs.sym("ibv_get_device_list"));
        ibv_open_device = reinterpret_cast<struct ibv_context *(*)(struct ibv_device *device)>(
            libibverbs.sym("ibv_open_device"));
        ibv_modify_qp = reinterpret_cast<int (*)(struct ibv_qp *qp, struct ibv_qp_attr *attr, int attr_mask)>(
            libibverbs.sym("ibv_modify_qp"));
        ibv_query_device = reinterpret_cast<int (*)(struct ibv_context *context, struct ibv_device_attr *device_attr)>(
            libibverbs.sym("ibv_query_device"));
        ibv_reg_mr = reinterpret_cast<struct ibv_mr *(*)(struct ibv_pd *pd, void *addr, size_t length, int access)>(
            libibverbs.sym("ibv_reg_mr"));
        rdma_bind_addr = reinterpret_cast<int (*)(struct rdma_cm_id *id, struct sockaddr *addr)>(
            librdmacm.sym("rdma_bind_addr"));
        rdma_create_event_channel = reinterpret_cast<struct rdma_event_channel *(*)(void)>(
            librdmacm.sym("rdma_create_event_channel"));
        rdma_create_id = reinterpret_cast<int (*)(struct rdma_event_channel *channel, struct rdma_cm_id **id, void *context, enum rdma_port_space ps)>(
            librdmacm.sym("rdma_create_id"));
        rdma_destroy_event_channel = reinterpret_cast<void (*)(struct rdma_event_channel *channel)>(
            librdmacm.sym("rdma_destroy_event_channel"));
        rdma_destroy_id = reinterpret_cast<int (*)(struct rdma_cm_id *id)>(
            librdmacm.sym("rdma_destroy_id"));
        // Prevent the libraries being closed, so that the symbols stay valid
        librdmacm.release();
        libibverbs.release();
    }
    catch (std::system_error &e)
    {
        init_result = std::current_exception();
        reset_stubs();
        log_warning("could not load ibverbs: %s", e.what());
    }
}

void ibv_loader_init()
{
    std::call_once(init_once, init);
    if (init_result)
        std::rethrow_exception(init_result);
}

} // namespace spead2

/* Wrappers in the global namespace. This is needed because ibv_exp_create_qp
 * calls ibv_create_qp, and so we need to provide an implementation.
 */
struct ibv_qp *ibv_create_qp(struct ibv_pd *pd, struct ibv_qp_init_attr *qp_init_attr)
{
    return spead2::ibv_create_qp(pd, qp_init_attr);
}

#endif // SPEAD2_USE_IBV
