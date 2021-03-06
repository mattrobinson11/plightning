from pytorch_lightning.plugins.ddp_plugin import DDPPlugin

import smdistributed.dataparallel.torch.distributed as dist
from smdistributed.dataparallel.torch.parallel.distributed import DistributedDataParallel as DDP

"""
torch.cuda.set_device
"""

class SagemakerDDPPlugin(DDPPlugin):

    def configure_ddp(
            self, model: LightningModule, device_ids: List[int]
    ) -> LightningDistributedDataParallel:
        """
        Pass through all customizations from constructor to `LightningDistributedDataParallel`.
        Override to define a custom DDP implementation.
        .. note:: Only requirement is that your DDP implementation subclasses LightningDistributedDataParallel
        The default implementation is::
            def configure_ddp(self, model, device_ids):
                model = LightningDistributedDataParallel(
                    model, device_ids=device_ids, find_unused_parameters=True
                )
                return model
        Args:
            model: the lightningModule
            device_ids: the list of devices available
        Returns:
            the model wrapped in LightningDistributedDataParallel
        """
        # if unset, default `find_unused_parameters` `True`
        #self._ddp_kwargs["find_unused_parameters"] = self._ddp_kwargs.get(
        #    "find_unused_parameters", True
        #)
        model = DDP(model)
        return model
        
    def init_ddp_connection(
            self,
            trainer,
            cluster_environment,
            global_rank: int,
            world_size: int,
            is_slurm_managing_tasks: bool = True,
    ) -> None:
      #if not torch_distrib.is_initialized():
      #    log.info(
      #        f"initializing ddp: GLOBAL_RANK: {global_rank}, MEMBER: {global_rank + 1}/{world_size}"
      #    )
      dist.init_process_group()
